from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
# Create your models here.



class User(AbstractUser):
    SUBSCRIBER = "SUBSCRIBER"
    CREATOR = "CREATOR"


    ROLE_CHOICES = [
        (SUBSCRIBER, "Abonne"),
        (CREATOR, "Createur"),
    ]


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=SUBSCRIBER,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    background_image = models.ImageField(
        upload_to="backgrounds/",
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de naissance",
    )
    location = models.CharField(
        
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Lieu de résidence",
    )
    follows = models.ManyToManyField(
        "self",
        symmetrical=False,
        limit_choices_to={'role': CREATOR},
        verbose_name="Abonnements",
    )

    def save(self, *args, **kwargs):
        if self.role == self.SUBSCRIBER:
            group = Group.objects.get(name="subscribers")
            group.user_set.add(self)
        else:
            group = Group.objects.get(name="creators")
            group.user_set.add(self)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.username

    