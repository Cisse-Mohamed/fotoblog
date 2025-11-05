from django.shortcuts import render, redirect
from .forms import PhotoForm, BlogForm, FollowUserForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView, DetailView, DeleteView, UpdateView
from .models import Photo, Blog
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.


def home(request):
    # Fetch the latest 5 blog posts
    blogs = Blog.objects.select_related('photo').filter(
        Q(contributors__in=request.user.follows.all()) | Q(starred=False)
    ).distinct().order_by('-date_created')

    # Fetch the latest 6 photos
    photos = Photo.objects.filter(
        Q(uploader__in=request.user.follows.all()) | ~Q(uploader=request.user)
    ).distinct().order_by('-date_created')
    context = {'blogs': blogs, 'photos': photos}
    return render(request, 'blog/home.html', context)

@login_required(login_url='blog:error404')
@permission_required('blog.add_photo', login_url='blog:error404')
def upload_photo(request):
   if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('blog:home')
   else:
       form = PhotoForm()
   return render(request, 'blog/upload_photo.html', {'form': form})


class error404View(TemplateView):
    template_name = 'blog/404.html'

@login_required(login_url='blog:error404')
@permission_required('blog.add_photo', login_url='blog:error404')
@permission_required('blog.add_blog', login_url='blog:error404')
def uploadphoto_and_blog(request):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        blog_form = BlogForm(request.POST)
        if photo_form.is_valid() and blog_form.is_valid():
            with transaction.atomic():
                photo_instance = photo_form.save(commit=False)
                photo_instance.uploader = request.user
                photo_instance.save()
                blog_instance = blog_form.save(commit=False)
                blog_instance.photo = photo_instance
                blog_instance.save()  # Save blog instance before adding to ManyToMany
                blog_instance.contributors.add(request.user, through_defaults={'contribution': 'Auteur principale'})
                return redirect('blog:home')
    else:
        photo_form = PhotoForm()
        blog_form = BlogForm()
    context = {
        'photo_form': photo_form,
        'blog_form': blog_form,
    }
    return render(request, 'blog/upload_photo_and_blog.html', context)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    permission_required = 'blog.delete_blog'
    login_url = 'blog:error404'
    raise_exception = True # Or handle permission denied in another way


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_update_form.html'
    permission_required = 'blog.change_blog'
    login_url = 'blog:error404'

    def get_success_url(self):
        blog_id = self.kwargs['pk']
        return reverse_lazy('blog:blog_detail', kwargs={'pk': blog_id})

@login_required(login_url='blog:error404')
@permission_required('blog.add_photo', login_url='blog:error404')
def upload_multiple_photos(request):
    PhotoFormSet = formset_factory(PhotoForm, extra=5)  # Allow uploading 3 photos at once
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo_instance = form.save(commit=False)
                    photo_instance.uploader = request.user
                    photo_instance.save()
            return redirect('blog:home')
    else:
        formset = PhotoFormSet()
    return render(request, 'blog/upload_multiple_photos.html', {'formset': formset})


class FollowUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['follows']
    template_name = 'blog/follow_user.html'
    success_url = reverse_lazy('blog:home')
    login_url = 'blog:error404'

    def get_object(self, queryset=None):
        # The object to update is the currently logged-in user
        return self.request.user

class DeleletePhotoView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'blog/photo_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    permission_required = 'blog.delete_photo'
    login_url = 'blog:error404'
    raise_exception = True # Or handle permission denied in another way


class UpdatePhotoView(PermissionRequiredMixin, UpdateView):
    model = Photo
    fields = ['image', 'caption']
    template_name = 'blog/photo_update_form.html'
    permission_required = 'blog.change_photo'
    login_url = 'blog:error404'

    def get_success_url(self):
        photo_id = self.kwargs['pk']
        return reverse_lazy('blog:home')