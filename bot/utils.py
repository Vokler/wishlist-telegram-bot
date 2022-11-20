from bot.models import User


def get_or_create_user(tg_chat_info):
    user, created = User.objects.get_or_create(
        username=tg_chat_info['username'], tg_chat_id=tg_chat_info['id'])
    return user
