# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=False, default=datetime.date.today)

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author)
    isbn = models.CharField(max_length=255)

    def __str__(self):
        return self.isbn

class SalesItem(models.Model):
    book = models.ForeignKey(Book)
    customer = models.CharField(max_length=255)
    item_price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer