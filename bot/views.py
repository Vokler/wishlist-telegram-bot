import json

from threading import Thread

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from telegram import Bot, Update

from bot.apps import BotConfig
from bot.handlers.start import start_handler
from bot.handlers.new_wish import new_wish_conv_handler
from bot.handlers.my_wishes import my_wishes_conv_handler
from bot.handlers.follow import follow_conv_handler
from bot.handlers.subscriptions import subs_conv_handler


@csrf_exempt
def process(request):
    bot = Bot(settings.BOT_TOKEN)
    update_queue = BotConfig.update_queue
    dispatcher = BotConfig.dispatcher

    # Register handlers here
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(new_wish_conv_handler)
    dispatcher.add_handler(my_wishes_conv_handler)
    dispatcher.add_handler(follow_conv_handler)
    dispatcher.add_handler(subs_conv_handler)

    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    update_queue.put(Update.de_json(json.loads(request.body.decode()), bot))

    return JsonResponse({})
