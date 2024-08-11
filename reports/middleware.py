import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user_from_token(token):
    user_model = get_user_model()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_model.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, user_model.DoesNotExist):
        return AnonymousUser()


class JwtAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = dict(
            (x.split("=") for x in scope["query_string"].decode().split("&"))
        )
        token = query_string.get("token", None)

        if not token:
            headers = dict(scope["headers"])
            token = headers.get(b"sec-websocket-protocol", b"").decode()

        scope["user"] = await get_user_from_token(token)
        return await self.app(scope, receive, send)
