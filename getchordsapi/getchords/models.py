from django.db import models
from django.utils import timezone

# Create your models here
class SongGenre(models.Model):
    genre_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'song_genre'


class SongCategory(models.Model):
    description = models.CharField(max_length=300)

    class Meta:
        db_table = 'song_category'


class SongMusician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    aditional_info = models.CharField(max_length=300)

    class Meta:
        db_table = 'song_musician'


class SongAlbum(models.Model):
    artist = models.ForeignKey(SongMusician, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

    class Meta:
        db_table = 'song_album'


class SongChords(models.Model):
    audio_file = models.FileField(default=None)
    chords = models.TextField(default="")
    sample_rate = models.IntegerField(default=0)
    song_lyric = models.TextField(default="")
    category_id = models.ForeignKey(SongCategory, on_delete=models.CASCADE)
    genre = models.ForeignKey(SongGenre, on_delete=models.CASCADE)
    album = models.ForeignKey(SongAlbum, on_delete=models.CASCADE)
    song_chord_type = models.CharField(max_length=20, default="")
    create_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'song_chords'

    class JSONAPIMeta:
        resource_name = 'audio_file'


class SongPlaylist(models.Model):
    playlist_name = models.CharField(max_length=100)
    song = models.ForeignKey(SongChords, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    mod_date = models.DateTimeField()

    class Meta:
        db_table = 'song_playlist'

