from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username


class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Book)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Item(models.Model):
    id_item = models.CharField(max_length=128)
    name_dish = models.CharField(max_length=128)
    price = models.FloatField()
    start_date = models.DateField()
    photo_item = models.ImageField(upload_to='image/%Y/%m/%d/')

    class META:
        ordering = ['id_item']

    def __unicode__(self):
        return self.id_item


class Order(models.Model):
    id_order = models.CharField(max_length=128)
    time_order = models.DateField()
    total = models.FloatField()

    class META:
        ordering = ['id_order']

    def __unicode__(self):
        return self.id_order


class OrderItem(models.Model):
    id_OI=models.CharField(max_length=128)
    id_item=models.ForeignKey(Item)
    id_order=models.ForeignKey(Order)
    item_total=models.IntegerField(default=0)

    class META:
        ordering=['id_OI']
    def __unicode__(self):
        return self.id_OI
    def total(self):
        return self.id_item.price*self.item_total
