import json
from threading import Thread

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update

from bot.apps import BotConfig
from bot.handlers.follow import follow_conv_handler
from bot.handlers.my_wishes import my_wishes_conv_handler
from bot.handlers.new_wish import new_wish_conv_handler
from bot.handlers.start import start_handler
from bot.handlers.subscriptions import subs_conv_handler

UPDATE_QUEUE = BotConfig.update_queue
DISPATCHER = BotConfig.dispatcher

THREAD = Thread(target=DISPATCHER.start, name='dispatcher')
THREAD.start()


@csrf_exempt
def process(request):
    bot = Bot(settings.BOT_TOKEN)

    # Register handlers here
    DISPATCHER.add_handler(start_handler)
    DISPATCHER.add_handler(new_wish_conv_handler)
    DISPATCHER.add_handler(my_wishes_conv_handler)
    DISPATCHER.add_handler(follow_conv_handler)
    DISPATCHER.add_handler(subs_conv_handler)

    UPDATE_QUEUE.put(Update.de_json(json.loads(request.body.decode()), bot))

    return JsonResponse({})
