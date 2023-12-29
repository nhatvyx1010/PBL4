# routing.py

from django.urls import path
from .consumers import YourConsumer  # Thay thế bằng consumer của bạn

websocket_urlpatterns = [
    path('ws/some_path/', YourConsumer.as_asgi()),  # Thay thế đường dẫn và consumer tương ứng
]
