import json
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
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.process_update(Update.de_json(json.loads(request.body.decode()), bot))

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    return JsonResponse({})
