from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from user.router import user_router
from aiCore.router import ai_core_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


api.add_router('', user_router)
api.add_router('', ai_core_router)