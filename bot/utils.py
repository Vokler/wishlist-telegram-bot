from bot.models import User


def get_or_create_user(tg_user_info):
    user, created = User.objects.get_or_create(username=tg_user_info['username'])
    return user
