import django.db as DD
import django.contrib.auth.models as DCAM

import games.models as GM


class GameListType(DD.models.Model):
    name = DD.models.CharField('Name', max_length=64)

    def __str__(self):
        return self.name


class GameInList(DD.models.Model):
    date = DD.models.DateField("Date", auto_now=False, auto_now_add=True)
    user = DD.models.ForeignKey(DCAM.User, on_delete=DD.models.CASCADE)
    game = DD.models.ForeignKey(GM.Game, on_delete=DD.models.CASCADE)
    game_list_type = DD.models.ForeignKey(
        GameListType, on_delete=DD.models.CASCADE)
    score = DD.models.IntegerField('Score', blank=True, null=True)
    finished = DD.models.DateField('Finished', blank=True, null=True)

    def __str__(self):
        return f'User: {self.user.username}. Game: {self.game}. Score: {self.score}'
