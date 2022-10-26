from django.core.management.base import BaseCommand

from bot.common import WishListBotCommands
from bot.tg_init import BOT


class Command(BaseCommand):

    def handle(self, *args, **options):
        commands = WishListBotCommands.create_bot_commands()
        result = BOT.set_my_commands(commands)

        success_msg = self.style.SUCCESS('Bot commands added successfully.')
        error_msg = self.style.ERROR('Something went wrong.')
        self.stdout.write(success_msg) if result else self.stdout.write(error_msg)
