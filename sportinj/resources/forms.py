from django import forms
from resources.models import Team
from django.core.validators import MinLengthValidator


class AddPlayerForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        max_length=255,
        label='Description',
        widget=forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        required=False
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label='Team is not selected',
        label='Team',
        widget=forms.Select(attrs={'class': 'form-control'})
    )