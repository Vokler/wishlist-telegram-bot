from enum import Enum

import telegram

from bot.utils import get_or_create_user


class WishListBotCommands(Enum):
    new_wish = ('new_wish', 'adding a new wish to your list')
    my_wishes = ('my_wishes', 'edit your wishes')
    follow = ('follow', 'subscribe to the user\'s wishes')
    subscriptions = ('subscriptions', 'your subscriptions to users')

    @classmethod
    def get_wishes_commands(cls):
        cmds = str(
            f'/{cls.new_wish.value[0]} - {cls.new_wish.value[1]}\n'
            f'/{cls.my_wishes.value[0]} - {cls.my_wishes.value[1]}\n'
        )
        return cmds

    @classmethod
    def get_users_commands(cls):
        cmds = str(
            f'/{cls.follow.value[0]} - {cls.follow.value[1]}\n'
            f'/{cls.subscriptions.value[0]} - {cls.subscriptions.value[1]}\n'
        )
        return cmds

    @classmethod
    def create_bot_commands(cls):
        commands = [telegram.BotCommand(command=cmd.value[0], description=cmd.value[1]) for cmd in cls]
        return commands


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
