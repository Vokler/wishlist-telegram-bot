import telegram
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot = telegram.Bot(settings.BOT_TOKEN)
        url = '{}{}'.format(settings.SERVER_DOMAIN, reverse('process'))
        is_appointed = bot.set_webhook(url=url)
        if is_appointed:
            self.stdout.write(self.style.SUCCESS('Webhook was successfully appointed.'))
        else:
            self.stdout.write(self.style.ERROR('Something went wrong.'))
