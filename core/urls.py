from django.urls import path
from rest_framework import routers

from core.views import SignUpView, LoginView, ProfileView, UpdatePasswordView

# user_router = routers.SimpleRouter()
# user_router.register('users', UserViewSet)

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]
# urlpatterns += user_router.urls
