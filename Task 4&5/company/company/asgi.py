"""
ASGI config for company project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# company/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core.consumers import DepartmentChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company.settings")

django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    path("ws/chat/", DepartmentChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})
