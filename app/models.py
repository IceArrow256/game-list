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
    name = models.CharField('Name',max_length=64, unique=True)
    def __str__(self):
        return self.name

class Developer(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=64, unique=True)
    def __str__(self):
        return self.name

class Game(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=64)
    release = models.DateField('Release')
    score = models.FloatField("Score", blank=True, null=True)
    def __str__(self):
        return self.name

class GameType(models.Model):
    name = models.CharField('Name', max_length=64)
    def __str__(self):
        return self.name

class GameList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    score = models.IntegerField('Score', blank=True)
    finished = models.DateField('Finished', blank=True, null=True)
    def __str__(self):
        return f'User: {self.user.username}. Game: {self.game}. Score: {self.score}'