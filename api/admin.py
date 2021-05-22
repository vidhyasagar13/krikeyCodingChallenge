# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from api.models import Author, SalesItem, Book

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(SalesItem)