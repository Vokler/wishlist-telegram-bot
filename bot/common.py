from enum import Enum

from bot.utils import get_or_create_user


class WishListBotCommands(Enum):
    new_wish = ('/new_wish', 'adding a new wish to your list')
    my_wishes = ('/my_wishes', 'edit your wishes')
    follow = ('/follow', 'subscribe to the user\'s wishes')
    subscriptions = ('/subscriptions', 'your subscriptions to users')

    @classmethod
    def get(cls):
        return '\n'.join(f'{command.value[0]} - {command.value[1]}' for command in cls)


class MyWishesStages(Enum):
    WISH_ITEMS_LIST = 'wish-items-list'
    WISH_ITEM_SETTINGS = 'wish-item-settings'
    WISH_ITEM_UPDATE = 'wish-item-update'
    WISH_ITEM_DELETE = 'wish-item-delete'


class MyWishesCallback(Enum):
    BACK_TO_WISH_ITEMS_LIST = 'back-to-wish-items-list'
    BACK_TO_WISH_ITEM = 'get-'


class AbsHandler:

    def __init__(self):
        self.user = None

    def start(self, update, context):
        self.user = get_or_create_user(update.message.from_user)
