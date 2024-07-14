from django import forms

from . import models


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = ['title', 'subtitle', 'text']
