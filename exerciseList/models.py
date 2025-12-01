from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Exercise(TimeStampedModel):
    class UnitType(models.TextChoices):
        REPS = "REPS", "Repetitions"
        SECONDS = "SECONDS", "Seconds"
        HOLD = "HOLD", "Isometric Hold"
        DISTANCE = "DISTANCE", "Distance"

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    summary = models.CharField(max_length=280, blank=True)
    instructions_md = models.TextField(blank=True)
    unit_type = models.CharField(max_length=16, choices=UnitType.choices, default=UnitType.REPS)
    default_sets = models.PositiveSmallIntegerField(default=3)
    default_reps_or_seconds = models.PositiveIntegerField(default=10)
    default_rest_sec = models.PositiveIntegerField(default=30)
    equipment = models.CharField(max_length=128, blank=True)

    camera_config_json = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self) -> str:
        return self.name


class ExerciseMedia(TimeStampedModel):
    class MediaType(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"

    exercise = models.ForeignKey("exerciseList.Exercise", on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=8, choices=MediaType.choices, default=MediaType.IMAGE)
    url = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=1)
    alt_text = models.CharField(max_length=140, blank=True)

    class Meta:
        unique_together = ("exercise", "order")
        ordering = ("order", "id")

    def __str__(self) -> str:
        return f"{self.exercise.name} • {self.media_type} • {self.order}"
