import logging
import time
from typing import Optional

from django.core.management import BaseCommand
from django.conf import settings
import json

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse, Message
from goals.models import Goal, GoalCategory
from todolist.settings import HOST

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options) -> None:
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started'))
        while True:
            res = self.tg_client.get_updates(offset=offset, allowed_updates='message')
            for item in res.result:
                offset = item.update_id + 1
                self.send_message(item.message)

    def send_message(self, message: Message) -> None:
        tg_user, _ = TgUser.objects.get_or_create(chat_id=message.chat.id, defaults={'username': message.chat.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(message.chat.id, f'Verification code: {tg_user.verification_code}')
        else:
            # self.tg_client.send_message(message.chat.id, f'User verified')
            self.handle_auth_user(tg_user, message)

    def handle_auth_user(self, tg_user: TgUser, message: Message):
        if message.text.startswith('/'):
            match message.text:
                case '/goals':
                    goals = self.get_goals(tg_user=tg_user)
                    self.tg_client.send_message(message.chat.id, goals)
                case '/create':
                    categories = self.get_categories(tg_user=tg_user)
                    categories_list = list(categories.keys())
                    if categories_list:
                        category = self.select_category(categories_list, tg_user=tg_user)
                        if category:
                            goal = self.create_new_goal(tg_user=tg_user, category=categories[category])
                            self.tg_client.send_message(tg_user.chat_id, goal)
                    else:
                        self.tg_client.send_message(message.chat.id, 'No categories available')

                case '/cancel':
                    pass
                case _:
                    self.tg_client.send_message(message.chat.id, 'Unknown command')

        else:
            self.tg_client.send_message(message.chat.id, 'No / in command')

    def get_goals(self, tg_user: TgUser) -> str:
        goals = Goal.objects.filter(
            user=tg_user.user,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)
        goals_list = [f'{goal.title}\n' for goal in goals]
        if goals_list:
            return ''.join(goals_list).rstrip()
        else:
            return 'Цели не найдены'

    def get_categories(self, tg_user: TgUser) -> dict:
        categories = GoalCategory.objects.filter(
            user=tg_user.user,
            is_deleted=False
        )
        return {category.title: category for category in categories}

    def select_category(self, categories_list, tg_user: TgUser) -> Optional[str]:
        category = ''
        categories = '\n'.join(categories_list)
        self.tg_client.send_message(tg_user.chat_id, f'Choose your category:{categories}')
        while category not in categories_list:
            time.sleep(10)
            category = self.tg_client.get_updates().result[-1].message.text
            if category in categories_list:
                self.tg_client.send_message(tg_user.chat_id, 'Category selected')
                return category
            elif category == '/cancel':
                self.tg_client.send_message(tg_user.chat_id, 'Operation cancelled')
                break
            else:
                self.tg_client.send_message(tg_user.chat_id, 'No such category')
        return None

    def create_new_goal(self, tg_user: TgUser, category: GoalCategory) -> str:
        goal_name = None
        while not goal_name:
            self.tg_client.send_message(tg_user.chat_id, 'Enter goal name')
            time.sleep(20)
            goal_name = self.tg_client.get_updates().result[-1].message.text
            if goal_name == '/cancel':
                return 'Goal creation was cancelled'
        goal = Goal.objects.create(category=category, title=goal_name, user=tg_user.user)
        goal_link = f'http://{HOST}/boards/{category.board.pk}/categories/{category.id}/goals?goal={goal.pk}'
        return goal_link


        # self.tg_client.send_message(message.chat.id, 'You are already verified')

        # self.tg_client.send_message(chat_id=message.chat.id, text=message.text)
