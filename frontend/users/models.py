from django.contrib.auth.models import AbstractUser
from django.db import models

from servers.models import Server

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class Action(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'


class User(AbstractUser):
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)
    actions = models.ManyToManyField(Action, blank=True)
    servers = models.ManyToManyField(Server, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
