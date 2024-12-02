from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class FundFamily(models.Model):
    name = models.CharField(max_length=255)

class MutualFund(models.Model):
    name = models.CharField(max_length=255)
    family = models.ForeignKey(FundFamily, on_delete=models.CASCADE, related_name='funds')
    nav = models.FloatField()  # Net Asset Value
    is_open_ended = models.BooleanField(default=False)

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    funds = models.ManyToManyField(MutualFund, through='Investment')

class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    amount = models.FloatField()
    purchased_on = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)