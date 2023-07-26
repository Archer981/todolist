import logging

from django.core.management import BaseCommand
from django.conf import settings
import json

from bot.tg.client import TgClient
from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_path = settings.BASE_DIR.joinpath('tg_get_response.json')
        send_path = settings.BASE_DIR.joinpath('tg_send_response.json')

        with open(get_path) as f:
            get_data = json.load(f)
            get_resp = GetUpdatesResponse(**get_data)
            print(get_resp)

        with open(send_path) as f:
            send_data = json.load(f)
            send_resp = SendMessageResponse(**send_data)
            print(send_resp)

        logger.debug('Ok')

        client = TgClient()
        print(client.get_updates())

# python manage.py test_bot
