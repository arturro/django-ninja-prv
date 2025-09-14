from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI(csrf=True, version="1.0")

# api.add_router("/tasks/", events_router)    # You can add a router as an object
api.add_router("/tasks/", "task.api.router", auth=JWTAuth(), tags=["Tasks"])  # or by Python path
api.add_router("/users/", "tenant.api.router", auth=JWTAuth(), tags=["Users"])  # or by Python path
api.add_router("/health_check/", "health_check.api.router")  # or by Python path
api.register_controllers(NinjaJWTDefaultController)
