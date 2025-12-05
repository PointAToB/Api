from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name


class Workout(TimeStampedModel):
    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    title = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    hero_image = models.URLField(blank=True)

    difficulty = models.CharField(max_length=16, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    genres = models.ManyToManyField(Genre, related_name="workouts", blank=True)

    is_published = models.BooleanField(default=True)
    estimated_minutes = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class WorkoutStep(TimeStampedModel):
    class Kind(models.TextChoices):
        EXERCISE = "EXERCISE", "Exercise"
        REST = "REST", "Rest"
        NOTE = "NOTE", "Note"

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField()
    kind = models.CharField(max_length=16, choices=Kind.choices)

    #if an EXERCISE:
    exercise = models.ForeignKey("exerciseList.Exercise", on_delete=models.PROTECT, null=True, blank=True, related_name="workout_steps")
    sets = models.PositiveSmallIntegerField(null=True, blank=True)
    reps_or_seconds = models.PositiveIntegerField(null=True, blank=True)
    rest_between_sets_sec = models.PositiveIntegerField(null=True, blank=True)
    tempo = models.CharField(max_length=32, blank=True)

    camera_required = models.BooleanField(default=False)
    camera_overrides_json = models.JSONField(null=True, blank=True, default=dict)

    #if REST:
    rest_duration_sec = models.PositiveIntegerField(null=True, blank=True)
    rest_message = models.CharField(max_length=200, blank=True)

    #if a NOTE:
    note_title = models.CharField(max_length=160, blank=True)
    note_body_md = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")
        unique_together = ("workout", "order")
        constraints = [
                                                        #EXERCISE requires exercise + sets + reps_or_seconds
            models.CheckConstraint(
                name="step_exercise_fields_valid",
                check=(
                    Q(kind="EXERCISE")
                    & Q(exercise__isnull=False)
                    & Q(sets__gt=0)
                    & Q(reps_or_seconds__gt=0)
                ) | Q(kind__in=["REST", "NOTE"]),
            ),

                                                            #REST requires duration
            models.CheckConstraint(
                name="step_rest_fields_valid",
                check=(Q(kind="REST") & Q(rest_duration_sec__gt=0)) | Q(kind__in=["EXERCISE", "NOTE"]),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.workout.title} • {self.kind} • {self.order}"


class WorkoutSession(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        ABANDONED = "ABANDONED", "Abandoned"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workout_sessions")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="sessions")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE)

    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    current_step_order = models.PositiveIntegerField(default=1)
    current_set_index = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workout"],
                condition=Q(status="ACTIVE"),
                name="uniq_active_session_per_workout",
            )
        ]


class CompletedSet(TimeStampedModel):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="completed_sets")
    workout_step = models.ForeignKey(WorkoutStep, on_delete=models.CASCADE, related_name="completed_sets")
    set_index = models.PositiveSmallIntegerField()
    reps_done = models.PositiveIntegerField(default=0)
    seconds_done = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("session", "workout_step", "set_index")
        ordering = ("workout_step", "set_index")

