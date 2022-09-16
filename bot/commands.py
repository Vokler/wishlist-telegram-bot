from enum import Enum


class WishListBotCommands(Enum):
    new_wish = ('/new_wish', 'adding a new wish to your list')
    my_wishes = ('/my_wishes', 'edit your wishes')

    @classmethod
    def get(cls):
        return '\n'.join(f'{command.value[0]} - {command.value[1]}' for command in cls)
