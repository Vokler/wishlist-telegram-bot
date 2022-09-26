from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from bot.common import WishListBotCommands, AbsHandler


class NewWishCommand(AbsHandler):
    TITLE, IMAGE, URL = range(3)

    def start(self, update, context):
        """Starts the conversation and asks the user about title of wish."""
        super(NewWishCommand, self).start(update, context)
        text = str('Alright, a new wish. What do you want to get? Please send me a name of your wish.')
        update.message.reply_text(text)
        return self.TITLE

    def title(self, update, context):
        """Stores the title and asks for an image."""
        title = update.message.text
        print(title)

        text = str('Good. Now, send me an image of your wish please, or send /skip if you don\'t want to.')
        update.message.reply_text(text)
        return self.IMAGE

    def image(self, update, context):
        """Stores the image and asks for an url."""
        image = update.message.photo[-1].get_file()
        print(image)

        text = str('Super. Now, send me an url of your wish if you have it, or send /skip.')
        update.message.reply_text(text)
        return self.URL

    def skip_image(self, update, context):
        """Skips the image and asks for an url."""
        print('User did not send an image.')

        text = str('OK. Now, send me an url of your wish if you have it, or send /skip.')
        update.message.reply_text(text)
        return self.URL

    def url(self, update, context):
        """Stores the url and ends the conversation."""
        url = update.message.text
        print(url)

        text = str('Thank you!')
        update.message.reply_text(text)
        return ConversationHandler.END

    def skip_url(self, update, context):
        """Skips the url and ends the conversation."""
        print('User did not send an url.')

        text = str('OK. Thank you!')
        update.message.reply_text(text)
        return ConversationHandler.END

    def cancel(self, update, context):
        """Cancels and ends the conversation."""
        return ConversationHandler.END


new_wish_cmd = NewWishCommand()
new_wish_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(WishListBotCommands.new_wish.name, new_wish_cmd.start)],
    states={
        new_wish_cmd.TITLE: [MessageHandler(Filters.text, new_wish_cmd.title)],
        new_wish_cmd.IMAGE: [
            MessageHandler(Filters.photo, new_wish_cmd.image),
            CommandHandler('skip', new_wish_cmd.skip_image)
        ],
        new_wish_cmd.URL: [
            MessageHandler(Filters.text & ~Filters.command, new_wish_cmd.url),
            CommandHandler('skip', new_wish_cmd.skip_url)
        ],
    },
    fallbacks=[CommandHandler('cancel', new_wish_cmd.cancel)]
)
