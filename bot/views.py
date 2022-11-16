import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from bot.tg_init import BOT, DISPATCHER, UPDATE_QUEUE


@csrf_exempt
def process(request):
    data = json.loads(request.body)
    update = Update.de_json(data, BOT)
    # DISPATCHER.process_update(update)
    UPDATE_QUEUE.put(update)

    return JsonResponse({})
