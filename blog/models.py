from django.db import models
from django.conf import settings

# Create your models here.

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, verbose_name='Legende')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Televerseur' )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de televersement')

    def __str__(self):
        return self.caption


class Blog(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Titre')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')
    starred = models.BooleanField(default=False, verbose_name='Etoile')
    count_word = models.PositiveIntegerField(default=0, blank=True, verbose_name="Nombre de mot")
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BlogContributor',
        related_name='contributions',
    )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.count_word = len(self.content.split())
        super().save(*args, **kwargs)


class BlogContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Utilisateur')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Blog')
    contribution = models.CharField(max_length=255, verbose_name='Contribution', blank=True)


    class Meta:
        unique_together = ('contributor', 'blog')



    def __str__(self):
        return f"{self.contributor.username} - {self.blog.title}"
