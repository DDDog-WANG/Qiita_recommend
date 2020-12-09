from django import forms

from .models import RawFromApi

class PostForm(forms.ModelForm):

    class Meta:
        model = RawFromApi
        fields = ('created_at', 'likes_count',)