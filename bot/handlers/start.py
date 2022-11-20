from telegram.constants import PARSEMODE_HTML
from telegram.ext import CommandHandler

from bot.common import WishListBotCommands
from bot.utils import get_or_create_user


def start(update, context):
    text = str(
        'I\'m <b>WishListBot</b> and I can help you to share your wishes or find out what others want to.\n\n'
        'You can control me by sending these commands:\n\n'
        '<b>Wishes</b>\n'
        f'{WishListBotCommands.get_wishes_commands()}\n'
        '<b>Users</b>\n'
        f'{WishListBotCommands.get_users_commands()}'

    )
    get_or_create_user(update.message.chat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=PARSEMODE_HTML)


start_handler = CommandHandler('start', start)
