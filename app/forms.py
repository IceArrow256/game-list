from django import forms
import app.models as models


class CountryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Country
        fields = ('name',)


class DeveloperCreateForm(forms.ModelForm):
    class Meta:
        model = models.Developer
        fields = ('country', 'name')


class PlatformCreateForm(forms.ModelForm):
    class Meta:
        model = models.Platform
        fields = ('name',)


class SeriesCreateForm(forms.ModelForm):
    class Meta:
        model = models.Series
        fields = ('name',)


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ('platform', 'series', 'developer', 'name', 'release')
        widgets = {
            'release': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
