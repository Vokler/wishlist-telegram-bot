import json

from queue import Queue
from threading import Thread

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from telegram.ext import CommandHandler, Dispatcher
from telegram import Bot, Update


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


@csrf_exempt
def process(request):
    bot = Bot(settings.BOT_TOKEN)
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue)

    # Register handlers here
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    update_queue.put(Update.de_json(json.loads(request.body.decode()), bot))

    return JsonResponse({})
