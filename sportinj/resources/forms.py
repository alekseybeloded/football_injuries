from django import forms
from resources.models import Team, Player



class AddPlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label='Team is not selected',
        label='Team',
    )

    class Meta:
        model = Player
        fields = [
            'name',
            'description',
            'team',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Player.objects.filter(name=name).exists():
            raise forms.ValidationError("User with that name already exists")