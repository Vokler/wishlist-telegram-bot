from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from django.contrib.auth.models import User

from bot.models import WishListItem
from bot.handlers.start import start_handler
from bot.common import MyWishesStages, MyWishesCallback

stages = MyWishesStages
callback = MyWishesCallback


class MyWishesCommand:
    def start(self, update, context):
        keyboard = self._get_wish_items_inline_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('Choose a wish from the list below:')
        update.message.reply_text(text, reply_markup=reply_markup)
        return stages.WISH_ITEMS_LIST.value

    def wish_items_list(self, update, context):
        query = update.callback_query
        query.answer()

        keyboard = self._get_wish_items_inline_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str('Choose a wish from the list below:')
        query.edit_message_text(text, reply_markup=reply_markup)
        return stages.WISH_ITEMS_LIST.value

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
                InlineKeyboardButton('« Back to Wish List', callback_data=callback.BACK_TO_WISH_ITEMS_LIST.value),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(
            f'Here it is: {wish_item.title}.\n'
            'What do you want to do with this wish?'
        )
        query.edit_message_text(text, reply_markup=reply_markup)
        return stages.WISH_ITEM_SETTINGS.value

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
        return stages.WISH_ITEM_UPDATE.value

    def wish_item_delete(self, update, context):
        query = update.callback_query
        query.answer()

        wish_item = WishListItem.objects.get(id=self._get_wish_item_id(query.data))
        # wish_item.delete() # todo: uncomment

        keyboard = [
            [InlineKeyboardButton('« Back to Wish List', callback_data=callback.BACK_TO_WISH_ITEMS_LIST.value)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(f'You have deleted {wish_item.title}.')
        query.edit_message_text(text, reply_markup=reply_markup)
        return stages.WISH_ITEM_DELETE.value

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
        pattern = f'{callback.BACK_TO_WISH_ITEM.value}{wish_item_id}'
        return pattern


cmd = MyWishesCommand()
my_wishes_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('my_wishes', cmd.start)],
    states={
        stages.WISH_ITEMS_LIST.value: [
            CallbackQueryHandler(cmd.wish_item),
        ],
        stages.WISH_ITEM_SETTINGS.value: [
            CallbackQueryHandler(cmd.wish_item_update, pattern='^edit-[0-9]+$'),
            CallbackQueryHandler(cmd.wish_item_delete, pattern='^delete-[0-9]+$'),
            CallbackQueryHandler(cmd.wish_items_list, pattern=callback.BACK_TO_WISH_ITEMS_LIST.value),
        ],
        stages.WISH_ITEM_DELETE.value: [
            CallbackQueryHandler(cmd.wish_items_list, pattern=callback.BACK_TO_WISH_ITEMS_LIST.value)
        ],
        stages.WISH_ITEM_UPDATE.value: [
            CallbackQueryHandler(cmd.wish_item, pattern=f'^{callback.BACK_TO_WISH_ITEM.value}[0-9]+$')
        ]
    },
    fallbacks=[CommandHandler('start', start_handler)]
)
