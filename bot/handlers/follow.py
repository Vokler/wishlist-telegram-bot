from django.conf import settings
from django.utils.translation import gettext_lazy as _
from telegram.constants import PARSEMODE_HTML
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler)

from bot.common import AbsHandler, WishListBotCommands
from bot.models import User, UserFollow


class FollowCommand(AbsHandler):
    SUBSCRIPTION = 'subscription'

    def start(self, update, context):
        """Starts the conversation and asks the user about the username of a user they want to subscribe to."""
        super(FollowCommand, self).start(update, context)
        text = _(
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
                text = _(f'Done. You\'ve subscribed to {tg_username}.')
                text_to_following = _(f'@{self.user.username} subscribed to you.')
                context.bot.send_message(chat_id=following.tg_chat_id, text=text_to_following)
            else:
                text = _(f'You\'ve already subscribed to {tg_username}.')
        except User.DoesNotExist:
            text = _(
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
    allow_reentry=True,
    entry_points=[CommandHandler(WishListBotCommands.follow.name, follow_cmd.start)],
    states={
        follow_cmd.SUBSCRIPTION: [MessageHandler(Filters.text, follow_cmd.create_subscription)],
    },
    fallbacks=[CommandHandler('cancel', follow_cmd.cancel)]
)
