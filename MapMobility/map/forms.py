from django import forms


class mapForm(forms.Form):
    date_field = forms.DateTimeField(label="Date",widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    lattitude = forms.FloatField(label='Lattitude')
    longitude = forms.FloatField(label='Longitude')