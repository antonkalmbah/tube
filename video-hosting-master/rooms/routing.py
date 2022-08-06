from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/media/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/private/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
