from django.contrib.auth.models import User
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import PARSEMODE_HTML
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from bot.common import (AbsHandler, MyWishesCallback, MyWishesStages,
                        WishListBotCommands)
from bot.handlers.start import start_handler
from bot.models import UserFollow, WishListItem


class SubscriptionsCommand(AbsHandler):
    SUBSCRIPTIONS = 'subscriptions'
    SUBSCRIPTION_SETTINGS = 'subscriptions-settings'

    def start(self, update, context):
        super(SubscriptionsCommand, self).start(update, context)
        keyboard = self._get_subscriptions()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('These are the users you are subscribed to:')
        update.message.reply_text(text, reply_markup=reply_markup)
        return self.SUBSCRIPTIONS

    def subscription(self, update, context):
        query = update.callback_query
        query.answer()

        subscription_id = query.data
        subscription = UserFollow.objects.get(id=subscription_id)

        keyboard = [
            [
                InlineKeyboardButton('Wishes', callback_data=f'wishes-{subscription_id}'),
                InlineKeyboardButton('Remove', callback_data=f'delete-{subscription_id}'),
            ],
            [
                InlineKeyboardButton('« Back to subscriptions', callback_data='prob'),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(
            f'Here it is: @{subscription.following.username}.\n'
            'What do you want to do with this subscription?'
        )
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.SUBSCRIPTION_SETTINGS

    def subscription_wishes(self, update, context):
        query = update.callback_query
        query.answer()

        subscription_id = self._get_subscription_id(query.data)
        subscription = UserFollow.objects.get(id=subscription_id)
        wish_items = subscription.following.wishlistitem_set.all()

        keyboard = [[InlineKeyboardButton('« Back to subscription', callback_data=f'prob')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if wish_items.exists():
            for item in wish_items:
                text = str(
                    f'<b>{item.title}</b>\n'
                    f'{item.url}\n'
                    f'{item.image.url if item.image else None}\n\n'
                )
                query.edit_message_text(text, reply_markup=reply_markup, parse_mode=PARSEMODE_HTML)
        else:
            text = 'Empty'

        return self.SUBSCRIPTION_SETTINGS

    def _get_subscriptions(self):
        subscriptions = self.user.who_is_followed.all()
        subscriptions_inline_keyboard = []
        for subscription in subscriptions:
            inline_keyboard = InlineKeyboardButton(f'@{subscription.following.username}', callback_data=subscription.id)
            subscriptions_inline_keyboard.append(inline_keyboard)
        keyboard = [subscriptions_inline_keyboard]
        return keyboard

    def _get_subscription_id(self, data):
        subscription_id = int(data.split('-')[1])
        return subscription_id

    # def _get_wish_item_pattern(self, wish_item_id):
    #     pattern = f'{callback.BACK_TO_WISH_ITEM.value}{wish_item_id}'
    #     return pattern


subs_cmd = SubscriptionsCommand()
subs_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(WishListBotCommands.subscriptions.name, subs_cmd.start)],
    states={
        subs_cmd.SUBSCRIPTIONS: [
            CallbackQueryHandler(subs_cmd.subscription),
        ],
        subs_cmd.SUBSCRIPTION_SETTINGS: [
            CallbackQueryHandler(subs_cmd.subscription_wishes, pattern='^wishes-[0-9]+$'),
        ]
    },
    fallbacks=[CommandHandler('start', start_handler)]
)
