from typing import Optional, Dict, List
from datetime import date
from ninja import Schema


class Macro(Schema):
    current: int
    goal: int


class NutritionLogOut(Schema):
    date: date
    calories: Macro
    carbs: Macro
    protein: Macro
    fiber: Macro
    fat: Macro


class NutritionUpdateIn(Schema):
    
    calories: Optional[int] = None
    carbs: Optional[int] = None
    protein: Optional[int] = None
    fiber: Optional[int] = None
    fat: Optional[int] = None

    add: Optional[Dict[str, int]] = None


class RecipeListItem(Schema):
    id: int
    title: str
    subtitle: str


class RecipeDetail(Schema):
    id: int
    title: str
    subtitle: str
    ingredients: List[str]
    steps: List[str]