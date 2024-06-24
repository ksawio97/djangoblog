from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(help_text='Maximum 200 characters')
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']