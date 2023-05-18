from django.urls import include, path

from core.ws import ChatConsumer

websocket_urlpatterns = [
    path('chat/<str:room_name>', ChatConsumer.as_asgi()),
]
