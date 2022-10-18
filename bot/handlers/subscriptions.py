from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import PARSEMODE_HTML
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler)

from bot.common import AbsHandler, WishListBotCommands
from bot.handlers.start import start_handler
from bot.models import UserFollow


class SubscriptionsCommand(AbsHandler):
    SUBSCRIPTIONS = 'subscriptions'
    SUBSCRIPTION = 'subscription'
    SUBSCRIPTION_WISHES = 'subscriptions-wishes'
    UNSUBSCRIBE = 'unsubscribe'

    BACK_TO_SUBSCRIPTION = 'back-to-subscription-'
    BACK_TO_SUBSCRIPTIONS = 'back-to-subscriptions'

    def start(self, update, context):
        super(SubscriptionsCommand, self).start(update, context)
        keyboard = self._get_subscriptions()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('These are the users you are subscribed to:')
        update.message.reply_text(text, reply_markup=reply_markup)
        return self.SUBSCRIPTIONS

    def subscriptions(self, update, context):
        query = update.callback_query
        query.answer()

        keyboard = self._get_subscriptions()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('These are the users you are subscribed to:')

        query.edit_message_text(text, reply_markup=reply_markup)
        return self.SUBSCRIPTIONS

    def subscription(self, update, context):
        query = update.callback_query
        query.answer()

        subscription_id = self._get_subscription_id(query.data)
        subscription = UserFollow.objects.get(id=subscription_id)

        keyboard = [
            [
                InlineKeyboardButton('Wishes', callback_data=f'wishes-{subscription_id}'),
                InlineKeyboardButton('Unsubscribe', callback_data=f'delete-{subscription_id}'),
            ],
            [
                InlineKeyboardButton('« Back to subscriptions', callback_data=self.BACK_TO_SUBSCRIPTIONS),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(
            f'Here it is: @{subscription.following.username}.\n'
            'What do you want to do with this subscription?'
        )
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.SUBSCRIPTION

    def subscription_wishes(self, update, context):
        query = update.callback_query
        query.answer()

        subscription_id = self._get_subscription_id(query.data)
        subscription = UserFollow.objects.get(id=subscription_id)
        wish_items = subscription.following.wishlistitem_set.all()

        keyboard = [[
            InlineKeyboardButton('« Back to subscription',
                                 callback_data=self._get_subscription_pattern(subscription_id))
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if wish_items.exists():
            text = ''
            for item in wish_items:
                wish_item_info = str(
                    f'<b>Title</b>: {item.title}\n'
                    f'<b>Image</b>: {"🖼" if item.image else "🚫"}\n'
                    f'<b>Url</b>: {item.url if item.url else "🚫"}\n\n'
                )
                text += wish_item_info
                query.edit_message_text(text, reply_markup=reply_markup, parse_mode=PARSEMODE_HTML)
        else:
            text = str(f'@{subscription.following.username} has not added any wishes yet.')
            query.edit_message_text(text, reply_markup=reply_markup, parse_mode=PARSEMODE_HTML)

        return self.SUBSCRIPTION_WISHES

    def subscription_remove(self, update, context):
        query = update.callback_query
        query.answer()

        subscription_id = self._get_subscription_id(query.data)
        subscription = UserFollow.objects.get(id=subscription_id)
        subscription.delete()

        keyboard = [
            [InlineKeyboardButton('« Back to subscriptions', callback_data=self.BACK_TO_SUBSCRIPTIONS)],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(f'You have unsubscribed from @{subscription.following.username}.')
        query.edit_message_text(text, reply_markup=reply_markup)

        return self.UNSUBSCRIBE

    def _get_subscriptions(self):
        subscriptions = self.user.who_is_followed.all()
        subscriptions_inline_keyboard = []
        for subscription in subscriptions:
            inline_keyboard = InlineKeyboardButton(f'@{subscription.following.username}', callback_data=subscription.id)
            subscriptions_inline_keyboard.append(inline_keyboard)
        keyboard = [subscriptions_inline_keyboard]
        return keyboard

    def _get_subscription_id(self, data):
        subscription_id = int(data.split('-')[-1])
        return subscription_id

    def _get_subscription_pattern(self, subscription_id):
        pattern = f'{self.BACK_TO_SUBSCRIPTION}{subscription_id}'
        return pattern


subs_cmd = SubscriptionsCommand()
subs_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(WishListBotCommands.subscriptions.name, subs_cmd.start)],
    states={
        subs_cmd.SUBSCRIPTIONS: [
            CallbackQueryHandler(subs_cmd.subscription),
        ],
        subs_cmd.SUBSCRIPTION: [
            CallbackQueryHandler(subs_cmd.subscription_wishes, pattern='^wishes-[0-9]+$'),
            CallbackQueryHandler(subs_cmd.subscription_remove, pattern='^delete-[0-9]+$'),
            CallbackQueryHandler(subs_cmd.subscriptions, pattern=subs_cmd.BACK_TO_SUBSCRIPTIONS),
        ],
        subs_cmd.SUBSCRIPTION_WISHES: [
            CallbackQueryHandler(subs_cmd.subscription, pattern=f'^{subs_cmd.BACK_TO_SUBSCRIPTION}[0-9]+$'),
        ],
        subs_cmd.UNSUBSCRIBE: [
            CallbackQueryHandler(subs_cmd.subscriptions, pattern=subs_cmd.BACK_TO_SUBSCRIPTIONS),
        ]
    },
    fallbacks=[CommandHandler('start', start_handler)]
)
