from telegram.ext import CommandHandler
from telegram.constants import PARSEMODE_HTML

from bot.utils import get_or_create_user
from bot.common import WishListBotCommands


def start(update, context):
    text = str(
        'I\'m <b>WishListBot</b> and I can help you to share your wishes or find out what others want to.\n\n'
        'You can control me by sending these commands:\n\n'
        f'{WishListBotCommands.get()}'
    )
    get_or_create_user(update.message.from_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=PARSEMODE_HTML)


start_handler = CommandHandler('start', start)
