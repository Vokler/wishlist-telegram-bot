from django.contrib.auth.models import User

from bot.models import WishListItem


def get_or_create_user(tg_user_info):
    user, created = User.objects.get_or_create(username=tg_user_info['username'])
    return user


def create_wish_item(wish_item_info, tg_user_info):
    user = get_or_create_user(tg_user_info)
    title = wish_item_info.get('Title')
    url = wish_item_info.get('Link')
    image = wish_item_info.get('Image')

    wish_item = {'title': title, 'url': url, 'image': image, 'user': user}
    WishListItem.objects.create(**wish_item)
