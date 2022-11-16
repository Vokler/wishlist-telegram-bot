from django.conf import settings
from telegram import Bot
from telegram.ext import Dispatcher

from bot.handlers.follow import follow_conv_handler
from bot.handlers.my_wishes import my_wishes_conv_handler
from bot.handlers.new_wish import new_wish_conv_handler
from bot.handlers.start import start_handler
from bot.handlers.subscriptions import subs_conv_handler


def telegram_bot():
    bot = Bot(settings.BOT_TOKEN)
    return bot


def telegram_dispatcher():
    bot = telegram_bot()
    dispatcher = Dispatcher(bot, None, workers=0)

    # Register handlers here

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(new_wish_conv_handler)
    dispatcher.add_handler(my_wishes_conv_handler)
    dispatcher.add_handler(follow_conv_handler)
    dispatcher.add_handler(subs_conv_handler)

    return dispatcher


BOT = telegram_bot()
DISPATCHER = telegram_dispatcher()
