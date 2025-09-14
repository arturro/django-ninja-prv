# from django.http import HttpRequest
# from ninja.security import HttpBearer
# from ninja_extra.auth.jwt import JWTAuth
#
# from .models import User
#
# class GlobalAuth(HttpBearer):
#     def authenticate(self, request: HttpRequest, token: str):
#         auth = JWTAuth()
#         try:
#             payload = auth.decode_token(token)
#             user_id = payload.get('user_id')
#             user = User.objects.get(id=user_id)
#             request.auth = user  # Attach the user to the request
#             return user
#         except Exception as e:
#             print(f"Authentication failed: {e}")
#             return None
