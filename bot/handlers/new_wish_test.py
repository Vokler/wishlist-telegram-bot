import logging

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler)

from bot.common import AbsHandler, WishListBotCommands
from bot.models import WishListItem


def start(update, context):
    """Starts the conversation and asks the user about title of wish."""
    text = str('Alright, a new wish. What do you want to get? Please send me a name of your wish.')
    update.message.reply_text(text)
    return 0


def title(update, context):
    """Stores the title and asks for an image."""
    title = update.message.text
    context.chat_data['title'] = title

    text = str('Good. Now, send me an image of your wish please, or send /skip if you don\'t want to.')
    update.message.reply_text(text)
    return 1


def image(update, context):
    """Stores the image and asks for an url."""
    image = update.message.photo[-1].get_file()
    context.chat_data['image_url'] = image['file_path']

    text = str('Super. Now, send me an url of your wish if you have it, or send /skip.')
    update.message.reply_text(text)
    return 2


def skip_image(update, context):
    """Skips the image and asks for an url."""
    print('User did not send an image.')

    text = str('OK. Now, send me an url of your wish if you have it, or send /skip.')
    update.message.reply_text(text)
    return 2


def url(update, context):
    """Stores the url and ends the conversation."""
    url = update.message.text
    context.chat_data['url'] = url

    _create_wish_item(context.chat_data)

    text = str('Thank you!')
    update.message.reply_text(text)
    return ConversationHandler.END


def skip_url(update, context):
    """Skips the url and ends the conversation."""
    print('User did not send an url.')

    _create_wish_item(context.chat_data)

    text = str('OK. Thank you!')
    update.message.reply_text(text)
    return ConversationHandler.END


def cancel(update, context):
    """Cancels and ends the conversation."""
    return ConversationHandler.END


def _create_wish_item(data):
    wish_item = WishListItem.objects.create(title=data.get('title'), url=data.get('url'), user=self.user)
    image_url = data.get('image_url')
    if image_url:
        wish_item.upload_image_by_url(image_url)
    return wish_item


ch = ConversationHandler(
    allow_reentry=True,
    entry_points=[CommandHandler(WishListBotCommands.new_wish.name, start)],
    states={
        0: [MessageHandler(Filters.text, title)],
        1: [
            MessageHandler(Filters.photo, image),
            CommandHandler('skip', skip_image)
        ],
        2: [
            MessageHandler(Filters.text & ~Filters.command, url),
            CommandHandler('skip', skip_url)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
