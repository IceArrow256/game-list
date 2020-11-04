from django.db import models
from django.contrib.auth.models import User


class Platform(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)

    def __str__(self):
        return self.name


class Developer(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=64, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, blank=True, null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=64)
    release = models.DateField('Release')
    score = models.FloatField("Score", blank=True, null=True)
    img = models.URLField("Image url", blank=True, null=True)
    class Meta:
        unique_together = ('developer', 'name')

    def __str__(self):
        return self.name
