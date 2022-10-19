import logging
import os
import urllib

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models

logger = logging.getLogger(__name__)


class User(AbstractUser):
    tg_chat_id = models.IntegerField(blank=True, null=True)


class WishListItem(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='wishlist_images', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def upload_image_by_url(self, url):
        result = urllib.request.urlretrieve(url)
        self.image.save(os.path.basename(url), File(open(result[0], 'rb')))


class UserFollow(models.Model):
    following = models.ForeignKey(to=User, related_name='who_follows', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=User, related_name='who_is_followed', on_delete=models.CASCADE)
