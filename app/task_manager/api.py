from django.utils import timezone

from ninja import NinjaAPI, Schema

# from task.api import router as events_router

api = NinjaAPI()
# api.add_router("/tasks/", events_router)    # You can add a router as an object
api.add_router("/tasks/", "task.api.router")  # or by Python path
api.add_router("/health_check/", "health_check.api.router")  # or by Python path
