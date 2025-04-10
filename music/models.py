from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='artist_profiles/', default='default.jpg')
    bio = models.TextField(blank=True)
    total_listens = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Listener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="listener")
    profile_picture = models.ImageField(upload_to='listener_profiles/', default='default.jpg')

    def __str__(self):
        return self.user.username

class Track(models.Model):
    GENRE_CHOICES = [
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('hiphop', 'Hip-Hop'),
        ('jazz', 'Jazz'),
        ('electronic', 'Electronic'),
        ('classical', 'Classical'),
        ('rnb', 'R&B'),
        ('country', 'Country'),
        ('reggae', 'Reggae'),
        ('metal', 'Metal'),
    ]

    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='tracks')
    audio_file = models.FileField(upload_to='tracks/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='pop')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='covers/',
                                    default='covers/default.jpg')

    def __str__(self):
        return f"{self.title} - {self.artist.user.username}"
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='albums/', null=True, blank=True)
    release_date = models.DateField()
    tracks = models.ManyToManyField(Track, related_name='albums')

    def __str__(self):
        return self.title
