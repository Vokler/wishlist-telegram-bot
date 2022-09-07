from django.db import models
from django.contrib.auth.models import User


class WishListItem(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='wishlist_images', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
