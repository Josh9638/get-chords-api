from django.urls import path
from . import views

urlpatterns = [
    path('chords/create_chord', views.songs_chords_register),
    path('chords/list', views.song_chords_list),
    path('chords/details/<int:pk>', views.song_chords_details),
    path('chord_analizer', views.chord_analizer)
]
