from django.contrib.auth.models import AnonymousUser
from ninja_jwt.tokens import AccessToken, TokenError

class JWTAuthMiddleware(object):
    def __init__(self, urls):
        self.urls = urls

    async def __call__(self, scope, receive, send):
        query = scope['query_string'].decode('utf8')
        token = query.split('token=')[1] if 'token=' in query else None

        try:
            access_token = AccessToken(token=token)
            scope['user'] = access_token['user_id']
        except TokenError:
            scope['user'] = AnonymousUser()






