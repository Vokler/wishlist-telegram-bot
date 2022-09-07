from telegram.ext import CommandHandler

from bot.utils import get_or_create_user


def start(update, context):
    text = str(
        'Hi! I\'m WishListBot and I will help you to share your wishes or find out what others want to.\n'
        'There are basic commands:\n'
        '/new_wish - adding a new wish to your list\n'
        '/update_wish - updating your exising wish\n'
    )
    get_or_create_user(update.message.from_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


start_handler = CommandHandler('start', start)
