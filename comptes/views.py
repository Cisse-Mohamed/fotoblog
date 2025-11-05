from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from . import forms



class CustomLoginView(LoginView):
    template_name = 'comptes/login.html'
    redirect_authenticated_user = True
    extra_context = {'title': 'Connexion'}


class CustomLogoutView(LogoutView):
    template_name = 'comptes/logout.html'
    extra_context = {'title': 'Déconnexion'}
# Additional context processors can be added here if needed


class SignupView(CreateView):
    template_name = 'comptes/signup.html'
    success_url = reverse_lazy('comptes:login')
    extra_context = {'title': 'Inscription'}

    # You would typically use a custom user creation form here
    form_class = forms.UserCreationFormWithAvatar

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'comptes/password_change_form.html'
    success_url = reverse_lazy('comptes:password_change_done')
    extra_context = {'title': 'Changer le mot de passe'}

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'comptes/password_change_done.html'
    extra_context = {'title': 'Mot de passe changé avec succès'}
# Additional context processors can be added here if needed


class AvatarUploadView(LoginRequiredMixin, UpdateView):
    form_class = forms.AvatarForm
    template_name = 'comptes/upload_avatar.html'
    success_url = reverse_lazy('blog:home')
    extra_context = {'title': 'Téléverser un avatar'}
    login_url = reverse_lazy('comptes:login')

    def get_object(self, queryset=None):
        return self.request.user