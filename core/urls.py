from rest_framework import routers

from core.views import UserViewSet

user_router = routers.SimpleRouter()
user_router.register('users', UserViewSet)

user_urlpatterns = [
]
user_urlpatterns += user_router.urls
