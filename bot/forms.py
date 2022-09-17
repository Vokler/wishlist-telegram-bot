from django.forms import ModelForm

from bot.models import WishListItem


class WishListItemForm(ModelForm):
    class Meta:
        model = WishListItem
        fields = ('title', 'url')
