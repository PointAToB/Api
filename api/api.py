from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from user.router import router
from nutritionLog.router import router as nutrition_router
from django.urls import path
from workoutLog.views import router as workouts_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


api.add_router('', router)
api.add_router('nutrition/', nutrition_router)
api.add_router("/workouts", workouts_router)