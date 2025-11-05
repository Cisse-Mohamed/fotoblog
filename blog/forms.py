from django import forms
from .models import Blog, Photo
from django.contrib.auth import get_user_model



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3}),
        }




class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class FollowUserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ['follows']
