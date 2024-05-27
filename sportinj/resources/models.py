from django.db import models
from django.urls import reverse


class Team(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['time_create']

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_uodate = models.DateTimeField(auto_now=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='teams')

    class Meta:
        ordering = ['time_create']

    def __str__(self) -> str:
        return self.name


class Injury(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    player = models.ForeignKey('Player', on_delete=models.PROTECT, related_name='players')

    class Meta:
        ordering = ['time_create']

    def __str__(self) -> str:
        return self.name
