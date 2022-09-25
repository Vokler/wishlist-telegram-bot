from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from django.contrib.auth.models import User

from bot.models import WishListItem
from bot.handlers.start import start_handler


class MyWishesCommand:
    # stages
    WISH_ITEMS_LIST, WISH_ITEM_SETTINGS, WISH_ITEM_UPDATE, WISH_ITEM_DELETE = range(4)

    # callback data
    BACK_TO_WISH_ITEMS_LIST = 'back-to-wish-items-list'
    BACK_TO_WISH_ITEM = 'get-'

    def start(self, update, context):
        keyboard = self._get_wish_items_inline_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('Choose a wish from the list below:')
        update.message.reply_text(text, reply_markup=reply_markup)
        return self.WISH_ITEMS_LIST

    def wish_items_list(self, update, context):
        query = update.callback_query
        query.answer()

        keyboard = self._get_wish_items_inline_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('Choose a wish from the list below:')
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.WISH_ITEMS_LIST

    def wish_item(self, update, context):
        query = update.callback_query
        query.answer()

        wish_item = WishListItem.objects.get(id=self._get_wish_item_id(query.data))

        keyboard = [
            [
                InlineKeyboardButton('Edit Wish', callback_data=f'edit-{wish_item.id}'),
                InlineKeyboardButton('Delete Wish', callback_data=f'delete-{wish_item.id}'),
            ],
            [
                InlineKeyboardButton('« Back to Wish List', callback_data=self.BACK_TO_WISH_ITEMS_LIST),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(
            f'Here it is: {wish_item.title}.\n'
            'What do you want to do with this wish?'
        )
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.WISH_ITEM_SETTINGS

    def wish_item_update(self, update, context):
        query = update.callback_query
        query.answer()

        wish_item_id = self._get_wish_item_id(query.data)
        wish_item = WishListItem.objects.get(id=wish_item_id)

        keyboard = [
            [
                InlineKeyboardButton('Edit Title', callback_data='edit-title'),
                InlineKeyboardButton('Edit Image', callback_data='edit-image')
            ],
            [
                InlineKeyboardButton('Edit Url', callback_data='edit-url')
            ],
            [
                InlineKeyboardButton('« Back to Wish', callback_data=self._get_wish_item_pattern(wish_item_id))
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(f'Edit {wish_item.title} info.')
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.WISH_ITEM_UPDATE

    def wish_item_delete(self, update, context):
        query = update.callback_query
        query.answer()

        wish_item = WishListItem.objects.get(id=self._get_wish_item_id(query.data))
        # wish_item.delete() # todo: uncomment

        keyboard = [
            [InlineKeyboardButton('« Back to Wish List', callback_data=self.BACK_TO_WISH_ITEMS_LIST)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(f'You have deleted {wish_item.title}.')
        query.edit_message_text(text, reply_markup=reply_markup)
        return self.WISH_ITEM_DELETE

    def _get_wish_items_inline_keyboard(self):
        user = User.objects.get(username='vokler')  # todo: replace on a real user
        wish_items = WishListItem.objects.filter(user=user)
        wish_items_inline_keyboard = []
        for item in wish_items:
            inline_keyboard = InlineKeyboardButton(item.title, callback_data=self._get_wish_item_pattern(item.id))
            wish_items_inline_keyboard.append(inline_keyboard)
        keyboard = [wish_items_inline_keyboard]
        return keyboard

    def _get_wish_item_id(self, data):
        wish_item_id = int(data.split('-')[1])
        return wish_item_id

    def _get_wish_item_pattern(self, wish_item_id):
        pattern = f'{self.BACK_TO_WISH_ITEM}{wish_item_id}'
        return pattern


cmd = MyWishesCommand()
my_wishes_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('my_wishes', cmd.start)],
    states={
        cmd.WISH_ITEMS_LIST: [
            CallbackQueryHandler(cmd.wish_item),
        ],
        cmd.WISH_ITEM_SETTINGS: [
            CallbackQueryHandler(cmd.wish_item_update, pattern='^edit-[0-9]+$'),
            CallbackQueryHandler(cmd.wish_item_delete, pattern='^delete-[0-9]+$'),
            CallbackQueryHandler(cmd.wish_items_list, pattern=cmd.BACK_TO_WISH_ITEMS_LIST),
        ],
        cmd.WISH_ITEM_DELETE: [
            CallbackQueryHandler(cmd.wish_items_list, pattern=cmd.BACK_TO_WISH_ITEMS_LIST)
        ],
        cmd.WISH_ITEM_UPDATE: [
            CallbackQueryHandler(cmd.wish_item, pattern=f'^{cmd.BACK_TO_WISH_ITEM}[0-9]+$')
        ]
    },
    fallbacks=[CommandHandler('start', start_handler)]
)
