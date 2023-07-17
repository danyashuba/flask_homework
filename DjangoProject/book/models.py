from django.db import models

import users.models


class Book(models.Model):
    book = models.TextField()
    user = models.ForeignKey(users.models.User,
                             related_name='books',
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'books'
