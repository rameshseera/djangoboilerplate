from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    singer = models.CharField(max_length=256, blank=True)
    logo = models.CharField(max_length=256, blank=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.title
    
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=256)
    minutes = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return str(self.album) + ' - ' + self.song_title