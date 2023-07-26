from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import BotVerificationSerializer
from bot.tg.client import TgClient


class BotVerificationView(generics.GenericAPIView):
    serializer_class = BotVerificationSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, *args, **kwargs) -> Response:
        serializer = BotVerificationSerializer(data=request.data)
        # if not serializer.is_valid():
        #     print(serializer.errors)
        serializer.is_valid(raise_exception=True)
        tg_user = TgUser.objects.get(verification_code=serializer.validated_data['verification_code'])
        tg_user.user = request.user
        tg_user.save()

        TgClient().send_message(tg_user.chat_id, 'Verification successful')
        return Response(serializer.data)
