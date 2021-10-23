from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

# Create your models here.
# TODO remove this user, not integrated well with django
#class User(models.Model):
#    username = models.CharField(max_length=20, primary_key=True)
#    password = models.CharField(max_length=20)
#    balance = models.IntegerField()


# class Investment(models.Model):
#     username = models.ForeignKey(
#         User, on_delete=models.CASCADE)
#     stock_symbol = models.CharField(max_length=20)
#     amount = models.IntegerField()
#     initial_value = models.IntegerField()
#     current_value = models.IntegerField()
#
#     class Meta:
#         unique_together = (("username", "stock_symbol"),)
