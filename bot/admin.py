from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bot.models import WishListItem


class WishListItemAdmin(admin.TabularInline):
    model = WishListItem
    fields = ('image', 'title', 'url')
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (WishListItemAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
