from django.utils import timezone

from ninja import NinjaAPI, Schema
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

# from task.api import router as events_router

api = NinjaExtraAPI()
# api.add_router("/tasks/", events_router)    # You can add a router as an object
api.add_router("/tasks/", "task.api.router")  # or by Python path
api.add_router("/health_check/", "health_check.api.router")  # or by Python path
api.register_controllers(NinjaJWTDefaultController)
