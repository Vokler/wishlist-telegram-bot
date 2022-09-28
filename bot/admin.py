from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bot.models import WishListItem, UserFollow


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


class UserAdmin(BaseUserAdmin):
    inlines = (WishListItemAdmin, WhoFollowAdmin, WhoIsFollowedAdmin)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
