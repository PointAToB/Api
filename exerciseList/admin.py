from django.contrib import admin
from .models import Exercise, ExerciseMedia

# Register your models here.
class ExerciseMediaInline(admin.TabularInline):
    model = ExerciseMedia
    extra = 0
    ordering = ("order",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "unit_type")
    search_fields = ("name", "slug")
    inlines = [ExerciseMediaInline]


@admin.register(ExerciseMedia)
class ExerciseMediaAdmin(admin.ModelAdmin):
    list_display = ("id", "exercise", "media_type", "order")
    list_filter = ("media_type",)
