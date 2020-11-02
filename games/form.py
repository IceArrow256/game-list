import django.forms as DF
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


SORT_CHOICES_ALL = [
    ('-score', 'Score (321)'),
    ('-release', 'Release (321)'),
    ("name", 'Name (ABC)'),
    ('platform__name', 'Platform (ABC)'),
    ('series__name', 'Series (ABC)'),
    ('developer__name', 'Developer (ABC)'),
    ('developer__country__name', 'Country (ABC)'),
    ('release', 'Release (123)'),
    ('score', 'Score (123)'),
    ("-name", 'Name (CBA)'),
    ('-platform__name', 'Platform (CBA)'),
    ('-series__name', 'Series (CBA)'),
    ('-developer__name', 'Developer (CBA)'),
    ('-developer__country__name', 'Country (CBA)'),
]

SORT_CHOICES_NAME = [
    ("name", 'Name (ABC)'),
    ("-name", 'Name (CBA)'),
]

SORT_CHOICES_COUNTRY = [
    ("name", 'Name (ABC)'),
    ('country__name', 'Country (ABC)'),
    ("-name", 'Name (CBA)'),
    ('-country__name', 'Country (CBA)'),
]


class FilterFormGames(DF.Form):
    search = DF.CharField(label='Search',
                          widget=DF.TextInput(attrs={'type': 'search',
                                                 'onsearch': 'form.submit()'}),
                          )
    sort = DF.ChoiceField(label='Sort',
                          widget=DF.Select(
                              attrs={'onchange': 'form.submit()'}),
                          choices=SORT_CHOICES_ALL,
                          initial='-score',
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
    release = DF.ChoiceField(label='Filter by Year',
                             widget=DF.Select(
                                 attrs={'onchange': 'form.submit()'}),
                             choices=get_years(),
                             required=False,
                             )
    not_in_my_list = DF.BooleanField(label='Hide My Game',
                                     widget=DF.CheckboxInput(
                                         attrs={'onchange': 'form.submit()'}),
                                     required=False,
                                     )


class FilterFormName(DF.Form):
    search = DF.CharField(label='Search',
                          widget=DF.TextInput(attrs={'type': 'search',
                                                 'onsearch': 'form.submit()'}),
                          )
    sort = DF.ChoiceField(label='Sort',
                          widget=DF.Select(
                                attrs={'onchange': 'form.submit()'}),
                          choices=SORT_CHOICES_NAME,
                          initial='name',
                          required=True,
                          )


class FilterFormContry(DF.Form):
    search = DF.CharField(label='Search',
                          widget=DF.TextInput(attrs={'type': 'search',
                                                 'onsearch': 'form.submit()'}),
                          )
    sort = DF.ChoiceField(label='Sort',
                          widget=DF.Select(
                                attrs={'onchange': 'form.submit()'}),
                          choices=SORT_CHOICES_COUNTRY,
                          initial='name',
                          required=True,
                          )
    country = DF.ModelChoiceField(label='Filter by Country',
                                  widget=DF.Select(
                                        attrs={'onchange': 'form.submit()'}),
                                  queryset=GM.Country.objects.all().order_by('name'),
                                  required=False,
                                  )


class CountryCreateForm(DF.ModelForm):
    class Meta:
        model = GM.Country
        fields = ('name',)


class DeveloperCreateForm(DF.ModelForm):
    class Meta:
        model = GM.Developer
        fields = ('country', 'name')


class PlatformCreateForm(DF.ModelForm):
    class Meta:
        model = GM.Platform
        fields = ('name',)


class SeriesCreateForm(DF.ModelForm):
    class Meta:
        model = GM.Series
        fields = ('name',)


class GameCreateForm(DF.ModelForm):
    class Meta:
        model = GM.Game
        fields = ('platform', 'series', 'developer', 'name', 'release')
        widgets = {
            'release': DF.DateInput(attrs={'type': 'date'}),
        }
