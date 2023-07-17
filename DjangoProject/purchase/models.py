from django.db import models

import users.models

import book.models


class Purchase(models.Model):
    date = models.DateField()
    user = models.ManyToManyField(users.models.User,
                                  related_name='purchases')
    book = models.ManyToManyField(book.models.Book,
                                  related_name='purchases')

    class Meta:
        db_table = 'purchases'
