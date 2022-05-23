from django.contrib import admin
from .models import SongCategory, SongGenre, SongAlbum, SongMusician

# Register your models here.
admin.site.register(SongCategory)
admin.site.register(SongGenre)
admin.site.register(SongAlbum)
admin.site.register(SongMusician)

