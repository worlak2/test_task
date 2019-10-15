from django import forms
from .models import VoteUser


class VoteAction(forms.ModelForm):
    class Meta:
        model = VoteUser
        fields = ['user', 'vote']
