from django.shortcuts import render
from typing import List, Optional
from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import Genre, Workout, WorkoutStep, WorkoutSession, CompletedSet
from .schemas import GenreOut, ExerciseOut, ExerciseMediaOut, WorkoutCardOut, WorkoutDetailOut, StepExerciseOut, StepRestOut, StepNoteOut, StepOut, SessionOut, SessionEventIn
from .utils import workout_percent
from user.models import User

# Create your views here.

router = Router(tags=["workouts"])  #--> /api/workouts


@router.get("/genres", response=List[GenreOut])
def list_genres(request):
    return list(Genre.objects.all().values("id", "name", "slug"))


@router.get("", response=List[WorkoutCardOut])
def list_workouts(request, genre: Optional[str] = None, difficulty: Optional[str] = None):
    if getattr(request, "user", None) and request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()

    qs = Workout.objects.prefetch_related("genres").filter(is_published=True)
    if genre:
        qs = qs.filter(genres__slug=genre)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    out: List[WorkoutCardOut] = []
    for w in qs:
        pct = workout_percent(user.id, w) if user else 0
        out.append(
            WorkoutCardOut(
                id=w.id,
                title=w.title,
                slug=w.slug,
                short_description=w.short_description or "",
                hero_image=w.hero_image or "",
                difficulty=w.difficulty,
                genres=[GenreOut(id=g.id, name=g.name, slug=g.slug) for g in w.genres.all()],
                percent_complete=pct,
            )
        )
    return out


@router.post("/sessions", response=SessionOut)
@transaction.atomic
def start_or_resume_session(request, workout_id: int):

    if getattr(request, "user", None) and request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()
        if not user:
            raise HttpError(400, "No users available for workout sessions")

    w = get_object_or_404(Workout, id=workout_id, is_published=True)

    session, created = WorkoutSession.objects.get_or_create(
        user=user,
        workout=w,
        status=WorkoutSession.Status.ACTIVE,
        defaults=dict(current_step_order=1, current_set_index=1),
    )

    if created:
        CompletedSet.objects.filter(session__user=user, session__workout=w).delete()

    pct = workout_percent(user.id, w)

    return SessionOut(
        id=session.id,
        workout_id=w.id,
        status=session.status,
        current_step_order=session.current_step_order,
        current_set_index=session.current_set_index,
        percent_complete=pct,
    )


@router.post("/sessions/{session_id}/events", response=SessionOut)
@transaction.atomic
def post_session_event(request, session_id: int, payload: SessionEventIn):

    if getattr(request, "user", None) and request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()
        if not user:
            raise HttpError(400, "No users available for workout sessions")

    session = get_object_or_404(
        WorkoutSession,
        id=session_id,
        user=user,
        status=WorkoutSession.Status.ACTIVE,
    )

    if payload.type == "complete_set":
        step = get_object_or_404(WorkoutStep, id=payload.workout_step_id, workout=session.workout, kind="EXERCISE")
        set_idx = payload.set_index or session.current_set_index
        CompletedSet.objects.get_or_create(
            session=session,
            workout_step=step,
            set_index=set_idx,
            defaults=dict(reps_done=payload.reps_done or 0, seconds_done=payload.seconds_done or 0),
        )
        if set_idx >= step.sets:
            session.current_step_order = step.order + 1
            session.current_set_index = 1
        else:
            session.current_set_index = set_idx + 1
        session.save(update_fields=["current_step_order", "current_set_index", "updated_at"])

    elif payload.type == "skip_step":
        step = get_object_or_404(WorkoutStep, id=payload.workout_step_id, workout=session.workout)
        session.current_step_order = step.order + 1
        session.current_set_index = 1
        session.save(update_fields=["current_step_order", "current_set_index", "updated_at"])

    elif payload.type in ("start_rest", "end_rest"):
        if payload.type == "end_rest" and payload.workout_step_id:
            step = get_object_or_404(WorkoutStep, id=payload.workout_step_id, workout=session.workout, kind="REST")
            session.current_step_order = step.order + 1
            session.current_set_index = 1
            session.save(update_fields=["current_step_order", "current_set_index", "updated_at"])

    #auto complete when beyond last step
    last_order = session.workout.steps.order_by("-order").values_list("order", flat=True).first() or 0
    if session.current_step_order > last_order:
        session.status = WorkoutSession.Status.COMPLETED
        session.ended_at = timezone.now()
        session.save(update_fields=["status", "ended_at", "updated_at"])

    pct = workout_percent(request.user.id, session.workout)
    return SessionOut(
        id=session.id,
        workout_id=session.workout_id,
        status=session.status,
        current_step_order=session.current_step_order,
        current_set_index=session.current_set_index,
        percent_complete=pct,
    )


@router.get("/{slug}", response=WorkoutDetailOut)
def get_workout(request, slug: str):
    if getattr(request, "user", None) and request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()

    w = get_object_or_404(
        Workout.objects.prefetch_related("genres", "steps__exercise", "steps__exercise__media"),
        slug=slug,
        is_published=True,
    )

    steps: List[StepOut] = []
    for s in w.steps.all():
        if s.kind == "EXERCISE":
            ex = s.exercise
            steps.append(
                StepExerciseOut(
                    kind="EXERCISE",
                    id=s.id,
                    order=s.order,
                    exercise=ExerciseOut(
                        id=ex.id,
                        name=ex.name,
                        slug=ex.slug,
                        summary=getattr(ex, "summary", "") or "",
                        instructions_md=getattr(ex, "instructions_md", "") or "",
                        unit_type=getattr(ex, "unit_type", "REPS"),
                        default_sets=getattr(ex, "default_sets", 0) or 0,
                        default_reps_or_seconds=getattr(ex, "default_reps_or_seconds", 0) or 0,
                        default_rest_sec=getattr(ex, "default_rest_sec", 0) or 0,
                        equipment=getattr(ex, "equipment", "") or "",
                        media=[
                            ExerciseMediaOut(
                                media_type=m.media_type, url=m.url, order=m.order, alt_text=m.alt_text or ""
                            )
                            for m in ex.media.all()
                        ],
                    ),
                    sets=s.sets,  #required by model constraint
                    reps_or_seconds=s.reps_or_seconds,  #also required by model constraint
                    rest_between_sets_sec=s.rest_between_sets_sec or getattr(ex, "default_rest_sec", 0) or 0,
                    tempo=s.tempo or "",
                    camera_required=bool(s.camera_required),
                )
            )
        elif s.kind == "REST":
            steps.append(
                StepRestOut(
                    kind="REST",
                    id=s.id,
                    order=s.order,
                    rest_duration_sec=s.rest_duration_sec or 0,
                    rest_message=s.rest_message or "",
                )
            )
        else:
            steps.append(
                StepNoteOut(
                    kind="NOTE",
                    id=s.id,
                    order=s.order,
                    note_title=s.note_title or "",
                    note_body_md=s.note_body_md or "",
                )
            )

    pct = workout_percent(user.id, w) if user else 0

    return WorkoutDetailOut(
        id=w.id,
        title=w.title,
        slug=w.slug,
        short_description=w.short_description or "",
        hero_image=w.hero_image or "",
        difficulty=w.difficulty,
        genres=[GenreOut(id=g.id, name=g.name, slug=g.slug) for g in w.genres.all()],
        steps=steps,
        percent_complete=pct,
    )

