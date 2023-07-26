from django.urls import path

from bot.apps import BotConfig
from bot.views import BotVerificationView

app_name = BotConfig.name

bot_urlpatterns = [
    path('verify', BotVerificationView.as_view(), name='verify'),
]
