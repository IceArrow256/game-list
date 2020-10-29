import django.forms as DF

import lists.models as LM
import games.models as GM


def get_years():
    data = GM.Game.objects.all().values("release").order_by('-release'),
    result = [(None, "---------")]
    for years in data:
        for year in years:
            value = (year['release'].year, year['release'].year)
            if value not in result:
                result.append(value)
    return result


def get_years_finished():
    years = LM.GameInList.objects.all().values("finished").order_by('-finished'),
    result = [(None, "---------")]
    for data in years:
        for year in data:
            if year['finished']:
                value = (year['finished'].year, year['finished'].year)
                if value not in result:
                    result.append(value)
    return result


SORT_CHOICES_ALL = [
    ('-finished', 'Finished (321)'),
    ('-game__release', 'Release (321)'),
    ("game__name", 'Game (ABC)'),
    ('game__platform__name', 'Platform (ABC)'),
    ('game__series__name', 'Series (ABC)'),
    ('game__developer__name', 'Developer (ABC)'),
    ('game__developer__country__name', 'Country (ABC)'),
    ('game_list_type', 'List (ABC)'),
    ('-score', 'Score (321)'),
    ('game__release', 'Release (123)'),
    ('finished', 'Finished (123)'),
    ("-game__name", 'Game (CBA)'),
    ('-game__platform__name', 'Platform (CBA)'),
    ('-game__series__name', 'Series (CBA)'),
    ('-game__developer__name', 'Developer (CBA)'),
    ('-game__developer__country__name', 'Country (CBA)'),
    ('-game_list_type', 'List (CBA)'),
    ('score', 'Score (123)'),
]


class FilterFormGamesInList(DF.Form):
    sort = DF.ChoiceField(label='Sort',
                          widget=DF.Select(
                              attrs={'onchange': 'form.submit()'}),
                          choices=SORT_CHOICES_ALL,
                          initial='-finished',
                          required=True,
                          )
    platform = DF.ModelChoiceField(label='Filter by Platform',
                                   widget=DF.Select(
                                       attrs={'onchange': 'form.submit()'}),
                                   queryset=GM.Platform.objects.all().order_by('name'),
                                   required=False,
                                   )
    series = DF.ModelChoiceField(label='Filter by Series',
                                 widget=DF.Select(
                                     attrs={'onchange': 'form.submit()'}),
                                 queryset=GM.Series.objects.all().order_by('name'),
                                 required=False,
                                 )
    developer = DF.ModelChoiceField(label='Filter by Developer',
                                    widget=DF.Select(
                                        attrs={'onchange': 'form.submit()'}),
                                    queryset=GM.Developer.objects.all().order_by('name'),
                                    required=False,
                                    )
    country = DF.ModelChoiceField(label='Filter by Country',
                                  widget=DF.Select(
                                      attrs={'onchange': 'form.submit()'}),
                                  queryset=GM.Country.objects.all().order_by('name'),
                                  required=False,
                                  )
    game_list_type = DF.ModelChoiceField(label='Filter by List',
                                         widget=DF.Select(
                                             attrs={'onchange': 'form.submit()'}),
                                         queryset=LM.GameListType.objects.all().order_by('name'),
                                         required=False,
                                         )
    release = DF.ChoiceField(label='Filter by Relese',
                             widget=DF.Select(
                                 attrs={'onchange': 'form.submit()'}),
                             choices=get_years(),
                             required=False,
                             )
    finished = DF.ChoiceField(label='Filter by Finished',
                             widget=DF.Select(
                                 attrs={'onchange': 'form.submit()'}),
                             choices=get_years_finished(),
                             required=False,
                             )


class GameInListCreateForm(DF.ModelForm):
    class Meta:
        model = LM.GameInList
        fields = ('game_list_type', 'score', 'finished')
        widgets = {
            'finished': DF.DateInput(attrs={'type': 'date'}),
        }
