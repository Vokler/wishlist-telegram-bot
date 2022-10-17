from queue import Queue

import telegram
from django.apps import AppConfig
from django.conf import settings
from telegram.ext import Dispatcher


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    fields = {}
    update_queue = Queue()

    @classproperty
    def dispatcher(cls):
        return cls.fields['dispatcher']

    def ready(self):
        bot = telegram.Bot(settings.BOT_TOKEN)
        self.fields['dispatcher'] = Dispatcher(bot, self.update_queue)
