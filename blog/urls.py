from django.urls import path
from . import views



app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('error404/', views.error404View.as_view(), name='error404'),
    path('upload_photo_and_blog/', views.uploadphoto_and_blog, name='upload_photo_and_blog'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('upload_multiple_photos/', views.upload_multiple_photos, name='upload_photos'),
    path('follow-user/', views.FollowUserView.as_view(), name='follow_user'),
    path('photo/<int:pk>/delete/', views.DeleletePhotoView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/update/', views.UpdatePhotoView.as_view(), name='photo_update'),





]