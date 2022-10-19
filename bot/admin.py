from django.contrib import admin
from django.contrib.auth.models import User

from bot.models import UserFollow, WishListItem


class WishListItemAdmin(admin.TabularInline):
    model = WishListItem
    fields = ('image', 'title', 'url')
    extra = 0


class WhoFollowAdmin(admin.TabularInline):
    model = UserFollow
    fields = ('following',)
    fk_name = 'follower'
    verbose_name = 'Following'
    verbose_name_plural = 'Followings'
    extra = 0


class WhoIsFollowedAdmin(admin.TabularInline):
    model = UserFollow
    fields = ('follower',)
    fk_name = 'following'
    verbose_name = 'Follower'
    verbose_name_plural = 'Followers'
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (WishListItemAdmin, WhoFollowAdmin, WhoIsFollowedAdmin)
