from django.conf import settings
from django.contrib.auth.models import User
from telegram.constants import PARSEMODE_HTML
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler)

from bot.common import AbsHandler, WishListBotCommands
from bot.models import UserFollow


class FollowCommand(AbsHandler):
    SUBSCRIPTION = 'subscription'

    def start(self, update, context):
        """Starts the conversation and asks the user about the username of a user they want to subscribe to."""
        super(FollowCommand, self).start(update, context)
        text = str(
            'Alright, let\'s add a new user to your subscription.\n'
            'Send me a telegram username of user in the following format: @username'
        )
        update.message.reply_text(text)
        return self.SUBSCRIPTION

    def create_subscription(self, update, context):
        """Stores the username and create UserFollow object."""
        tg_username = update.message.text
        username = tg_username.strip('@')
        try:
            following = User.objects.get(username=username)
            subscription, created = UserFollow.objects.get_or_create(follower=self.user, following=following)
            if created:
                text = str(f'Done. You\'ve subscribed to {tg_username}.')
                # todo: send notification to tg_username about new follower
            else:
                text = str(f'You\'ve already subscribed to {tg_username}.')
        except User.DoesNotExist:
            text = str(
                f'{tg_username} does not use <b>WishListBot</b> bot.\n\n'
                f'Share the link: {settings.BOT_LINK}'
            )
        update.message.reply_text(text, parse_mode=PARSEMODE_HTML)
        return ConversationHandler.END

    def cancel(self, update, context):
        """Cancels and ends the conversation."""
        return ConversationHandler.END


follow_cmd = FollowCommand()
follow_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(WishListBotCommands.follow.name, follow_cmd.start)],
    states={
        follow_cmd.SUBSCRIPTION: [MessageHandler(Filters.text, follow_cmd.create_subscription)],
    },
    fallbacks=[CommandHandler('cancel', follow_cmd.cancel)]
)
