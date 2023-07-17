from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = 'user'
