from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from user.router import router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


api.add_router('', router)