# asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from myweb.routing import websocket_urlpatterns  # Thay thế bằng đường dẫn đến file routing của bạn

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
