from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class BotVerificationSerializer(serializers.ModelSerializer):
    tg_id = serializers.IntegerField(source='chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'verification_code', 'user_id', 'username')
        read_only_fields = ('tg_id', 'user_id', 'username')

    def validate_verification_code(self, entered_code: str) -> str:
        try:
            self.tg_user = TgUser.objects.get(verification_code=entered_code)
        except TgUser.DoesNotExist:
            raise ValidationError('Verification code not correct')
        return entered_code
