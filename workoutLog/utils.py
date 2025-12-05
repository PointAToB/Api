from django.db.models import Sum
from .models import Workout, CompletedSet


def workout_total_sets(workout: Workout) -> int:
    return workout.steps.filter(kind="EXERCISE").aggregate(total=Sum("sets"))["total"] or 0


def workout_completed_sets(user_id: int, workout_id: int) -> int:
    return (
        CompletedSet.objects
        .filter(session__user_id=user_id, session__workout_id=workout_id)
        .values("workout_step_id", "set_index")
        .distinct()
        .count()
    )


def workout_percent(user_id: int, workout: Workout) -> int:
    total = workout_total_sets(workout)
    if total == 0:
        return 0
    done = workout_completed_sets(user_id, workout.id)
    pct = round(100 * done / total)
    return max(0, min(100, pct))
