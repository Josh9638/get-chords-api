from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import SongGenre, SongCategory, SongAlbum, SongMusician, SongChords, SongPlaylist
from django.contrib.auth.models import User
from .serializers import SongGenreSerializer, SongCategorySerializer, SongAlbumSerializer, SongMusicianSerializer, SongChordsSerializer, SongPlaylistSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
import os
import vamp
import librosa
from getchordsapi import settings
from django.db import connection
from urllib.parse import unquote


# Create your views here.
class SongChordsRegisterApiView(APIView):
    serializer_class = SongChordsSerializer

    def post(self, request):
        chords_of_song = self.serializer_class(data=request.data)

        if chords_of_song.is_valid():
            chords_of_song.save()

            audio_file_path = chords_of_song.data['audio_file']
            audio_name = os.path.basename(audio_file_path)

            #parseamos codigo unicode en ascii
            audio_name = unquote(audio_name)

            #cargamos audio, obtenemos el audio data y el sample rate y luego obtenemos los acordes con vamp
            audio_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, audio_name)
            data, rate = librosa.load(audio_path)
            #print('\n')
            #print(data)
            #print('\n')
            chords_gen = vamp.process_audio(data, rate, 'nnls-chroma:chordino')

            #actualizamos el registro de SongChords
            chords_songs_updated = update_song_chords(chords_of_song.data['id'], audio_name, rate, list(chords_gen))

            #eliminamos archivo de audio
            os.remove(audio_path)

            return Response(chords_songs_updated.data, status=status.HTTP_201_CREATED)
        else:
            return Response(chords_of_song.errors, status=status.HTTP_400_BAD_REQUEST)


songs_chords_register = SongChordsRegisterApiView.as_view()


class SongChordsListView(generics.ListAPIView):
    queryset = SongChords.objects.all()
    serializer_class = SongChordsSerializer

song_chords_list = SongChordsListView.as_view()


class SongChordsDetails(APIView):
    def get_song_chords(self, pk):
        try:
            return SongChords.objects.get(pk=pk)
        except SongChords.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        song_chords = self.get_song_chords(pk)
        serializer_class = SongChordsSerializer(song_chords)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        song_chords = self.get_song_chords(pk)
        serializer_class = SongChordsSerializer(song_chords, data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        song_chords = self.get_song_chords(pk)
        song_chords.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


song_chords_details = SongChordsDetails.as_view()


def update_song_chords(id, audio_name, sample_rate, chords):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE song_chords SET audio_file = %s, chords = %s, sample_rate = %s WHERE id = %s", [audio_name, str(chords), sample_rate, id])

    #song_chords = SongChords()
    #song_chords.id = id
    #song_chords.audio_file = audio_name
    #song_chords.chords = chords
    #song_chords.sample_rate = sample_rate
    song_chords = SongChords.objects.get(id=id)

    serializer_class = SongChordsSerializer(song_chords)

    return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)





