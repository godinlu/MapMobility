from django import forms


class mapForm(forms.Form):
    date_field = forms.DateTimeField(
        label="date",
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    lattitude = forms.FloatField(label='lattitude')
    longitude = forms.FloatField(label='longitude')