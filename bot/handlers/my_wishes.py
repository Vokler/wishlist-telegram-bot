from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)
from telegram.constants import PARSEMODE_HTML

from django.contrib.auth.models import User

from bot.models import WishListItem
from bot.handlers.start import start_handler
from bot.common import MyWishesStages, MyWishesCallback

stages = MyWishesStages
callback = MyWishesCallback


class WishItemUpdate:
    UPDATING_FIELD = 'updating-field'

    def start(self, update, context):
        query = update.callback_query
        query.answer()
        field = self._get_editable_field(query.data)
        context.chat_data.update({
            'field': field,
            'wish_item_id': self._get_wish_item_id(query.data),
        })

        text = str(f'OK. Send me the new {field} for your wish.')
        query.edit_message_text(text)
        return self.UPDATING_FIELD

    def update(self, update, context):
        new_value = update.message.text
        field = context.chat_data['field']
        obj_id = context.chat_data['wish_item_id']

        # updating process
        obj = WishListItem.objects.get(id=obj_id)
        setattr(obj, field, new_value)
        obj.save()

        keyboard = [
            [
                InlineKeyboardButton('« Back to Wish', callback_data=f'{callback.BACK_TO_WISH_ITEM.value}{obj_id}'),
                # InlineKeyboardButton('« Back to Wish List', callback_data=callback.BACK_TO_WISH_ITEMS_LIST.value)
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(f'Success! The {field} updated.')
        update.message.reply_text(text, reply_markup=reply_markup)
        return stages.WISH_ITEM_UPDATE.value

    def _get_editable_field(self, data):
        field = data.split('-')[2]
        return field

    def _get_wish_item_id(self, data):
        id = data.split('-')[1]
        return id


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
                InlineKeyboardButton('Edit Title', callback_data=f'edit-{wish_item_id}-title'),
                InlineKeyboardButton('Edit Image', callback_data=f'edit-{wish_item_id}-image')
            ],
            [
                InlineKeyboardButton('Edit Url', callback_data=f'edit-{wish_item_id}-url')
            ],
            [
                InlineKeyboardButton('« Back to Wish', callback_data=self._get_wish_item_pattern(wish_item_id))
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = str(
            f'Edit {wish_item.title} info.\n\n'
            f'<b>Title</b>: {wish_item.title}\n'
            f'<b>Image</b>: None\n'
            f'<b>Url</b>: {wish_item.url if wish_item.url else None}\n'
        )
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode=PARSEMODE_HTML)
        return stages.WISH_ITEM_UPDATE.value

    def wish_item_delete(self, update, context):
        query = update.callback_query
        query.answer()

        wish_item = WishListItem.objects.get(id=self._get_wish_item_id(query.data))
        wish_item.delete()

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
wish_item_update = WishItemUpdate()

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
            CallbackQueryHandler(cmd.wish_item, pattern=f'^{callback.BACK_TO_WISH_ITEM.value}[0-9]+$'),
            CallbackQueryHandler(wish_item_update.start, pattern='^edit-[0-9]+-[a-z]+$')
        ],

        # WishItemUpdate
        wish_item_update.UPDATING_FIELD: [
            MessageHandler(Filters.text, wish_item_update.update),
            CallbackQueryHandler(cmd.wish_item, pattern=f'^{callback.BACK_TO_WISH_ITEM.value}[0-9]+$'),
        ]
    },
    fallbacks=[CommandHandler('start', start_handler)]
)
