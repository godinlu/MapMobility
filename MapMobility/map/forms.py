from django import forms
from datetime import datetime


class DateForm(forms.Form):
    date_field = forms.DateTimeField(
        label="date",
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=datetime.now()
    )