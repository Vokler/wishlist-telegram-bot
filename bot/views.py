import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from bot.tg_init import BOT, DISPATCHER

logger = logging.getLogger(__name__)


@csrf_exempt
def process(request):
    logger.warning(f'REQUEST: {request.body.decode()}')
    data = json.loads(request.body.decode())
    update = Update.de_json(data, BOT)
    try:
        DISPATCHER.process_update(update)
    except Exception as e:
        logger.warning(f'ERROR: {e}')

    return JsonResponse({})
