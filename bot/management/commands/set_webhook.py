from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from bot.tg_init import BOT


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = '{}{}'.format(settings.SERVER_DOMAIN, reverse('process'))
        is_appointed = BOT.set_webhook(url=url)
        if is_appointed:
            self.stdout.write(self.style.SUCCESS('Webhook was successfully appointed.'))
        else:
            self.stdout.write(self.style.ERROR('Something went wrong.'))
