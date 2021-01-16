from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Location(models.Model):
    user=models.ForeignKey(User,related_name='cities',on_delete=models.CASCADE,)
    name=models.CharField(max_length=250, unique=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # new
        return reverse('index')
