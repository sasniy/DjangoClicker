from django.db import models
from django.contrib.auth.models import User


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    click_power = models.PositiveIntegerField(default=1)
# Create your models here.
