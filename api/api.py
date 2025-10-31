from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from user.router import router
from nutritionLog.router import router as nutrition_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


api.add_router('', router)
api.add_router('nutrition/', nutrition_router)
