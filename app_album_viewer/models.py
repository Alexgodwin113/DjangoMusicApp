
from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



class Album(models.Model):
    DEFAULT_COVER = 'static/css/defaultcover.avif'
    FORMAT_CHOICES = [
        ('Digital download', 'Digital download'),
        ('CD', 'CD'),
        ('Vinyl', 'Vinyl'),
    ]

    title = models.CharField(max_length=128, unique=False)
    description = models.TextField(blank=True)
    artist = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    release_date = models.DateField(null=True, blank=True)
    
    def validate_release_date(self):
        current_date = timezone.now().date()
        future_limit = current_date + timezone.timedelta(days=3 * 365)

        if self.release_date is not None:
            release_date = (
                self.release_date if isinstance(self.release_date, date)
                else datetime.strptime(str(self.release_date), '%Y-%m-%d').date()
            )

            if release_date > future_limit:
                self.release_date = future_limit
            elif release_date > current_date and release_date.month != 1:
                self.release_date = release_date.replace(month=1)

    def save(self, *args, **kwargs):
        self.validate_release_date()
        super().save(*args, **kwargs)
    
    
    cover_art = models.ImageField(upload_to='sample_data', default=DEFAULT_COVER, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.title
    
    def get_comments(self):
        return UserComment.objects.filter(album=self)
    
    def add_comment(self, user, message):
        UserComment.objects.create(user=user, album=self, message=message)
        
    def cover_art_url(self):
        if self.cover_art:
            return self.cover_art.url
        else:
            return Album.DEFAULT_COVER

class Song(models.Model):
    title = models.CharField(max_length=128)
    runtime = models.IntegerField()  # Assuming runtime is in seconds
    albums = models.ManyToManyField(Album)
    def __str__(self):
        return self.title

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.album.title}: {self.message}"

