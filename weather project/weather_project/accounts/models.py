from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser

# Create your models here.

class User(User, AbstractUser):
    pass
    def __str__(self):
        return "@{}".format(self.username)
