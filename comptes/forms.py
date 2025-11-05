from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms




class UserCreationFormWithAvatar(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name','email','role',
                   "date_of_birth", "location",'password1', 'password2')


class AvatarForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar']

