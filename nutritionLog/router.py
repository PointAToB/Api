from typing import List
from http import HTTPStatus
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import NutritionLog, Recipe
from .schema import (
    NutritionLogOut, NutritionUpdateIn,
    RecipeListItem, RecipeDetail
)

router = Router(tags=['nutrition'])


def _today_log(user) -> NutritionLog:
    log, _ = NutritionLog.objects.get_or_create(user=user, date=timezone.localdate())
    return log


def _serialize(log: NutritionLog) -> dict:
    return {
        "date": log.date,
        "calories": {"current": log.calories_current, "goal": log.calories_goal},
        "carbs":    {"current": log.carbs_current,    "goal": log.carbs_goal},
        "protein":  {"current": log.protein_current,  "goal": log.protein_goal},
        "fiber":    {"current": log.fiber_current,    "goal": log.fiber_goal},
        "fat":      {"current": log.fat_current,      "goal": log.fat_goal},
    }


def _seed_recipe_once():
    if not Recipe.objects.exists():
        Recipe.objects.create(
            title="Scrambled Madness",
            subtitle="A protein-rich breakfast",
            meal_type="BREAKFAST",
            ingredients=["3 eggs", "Cheese", "Turkey slices", "Salt and pepper"],
            steps=[
                "Start by heating up a pan to medium heat",
                "Add a teaspoon of butter",
                "Add all eggs"
            ],
        )


@router.get('log', auth=JWTAuth(), response=NutritionLogOut)
def get_log(request):
    return _serialize(_today_log(request.user))


@router.put('log', auth=JWTAuth(), response={HTTPStatus.OK: NutritionLogOut})
def update_log(request, payload: NutritionUpdateIn):
    log = _today_log(request.user)
    data = payload.dict(exclude_none=True)
    inc  = data.pop('add', None)

    if inc:
        for k, v in inc.items():
            if k == 'calories': log.calories_current += v
            elif k == 'carbs': log.carbs_current += v
            elif k == 'protein': log.protein_current += v
            elif k == 'fiber': log.fiber_current += v
            elif k == 'fat': log.fat_current += v

    for k, v in data.items():
        if k == 'calories': log.calories_current = v
        elif k == 'carbs': log.carbs_current = v
        elif k == 'protein': log.protein_current = v
        elif k == 'fiber': log.fiber_current = v
        elif k == 'fat': log.fat_current = v

    log.save()
    return _serialize(log)


@router.post('reset', auth=JWTAuth(), response={HTTPStatus.OK: NutritionLogOut})
def reset_log(request):
    log = _today_log(request.user)
    log.calories_current = log.carbs_current = log.protein_current = log.fiber_current = log.fat_current = 0
    log.save()
    return _serialize(log)


@router.get('recipes', auth=JWTAuth(), response=List[RecipeListItem])
def list_recipes(request):
    _seed_recipe_once()
    return [RecipeListItem(id=r.id, title=r.title, subtitle=r.subtitle) for r in Recipe.objects.all()]


@router.get('recipes/{recipe_id}', auth=JWTAuth(), response=RecipeDetail)
def recipe_detail(request, recipe_id: int):
    _seed_recipe_once()
    r = get_object_or_404(Recipe, id=recipe_id)
    return RecipeDetail(id=r.id, title=r.title, subtitle=r.subtitle, ingredients=r.ingredients, steps=r.steps)