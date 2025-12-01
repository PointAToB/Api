from django.contrib import admin
from .models import Genre, Workout, WorkoutStep, WorkoutSession, CompletedSet

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")


class WorkoutStepInline(admin.TabularInline):
    model = WorkoutStep
    extra = 0
    ordering = ("order",)
    fields = (
        "order", "kind",
        "exercise", "sets", "reps_or_seconds", "rest_between_sets_sec", "tempo",
        "camera_required",
        "rest_duration_sec", "rest_message",
        "note_title", "note_body_md",
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "difficulty", "is_published")
    list_filter = ("difficulty", "is_published", "genres")
    search_fields = ("title", "slug")
    filter_horizontal = ("genres",)
    inlines = [WorkoutStepInline]


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workout", "status", "current_step_order", "current_set_index")
    list_filter = ("status",)


@admin.register(CompletedSet)
class CompletedSetAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "workout_step", "set_index", "reps_done", "seconds_done")
    list_filter = ("workout_step",)

