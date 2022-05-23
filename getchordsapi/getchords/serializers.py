from rest_framework import serializers
from .models import SongCategory, SongGenre, SongMusician, SongAlbum, SongChords, SongPlaylist
from django.contrib.auth.models import User


class SongCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SongCategory
        fields = '__all__'


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = '__all__'


class SongMusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongMusician
        fields = '__all__'


class SongAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongAlbum
        fields = '__all__'


class SongChordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongChords
        fields = ('id','audio_file','chords','sample_rate','song_lyric','category_id','genre','album','song_chord_type', 'create_date', 'mod_date')
        #fields = '__all__'


class SongPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongPlaylist
        fields = '__all__'


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}
        ordering = ['id']

    def create(self, validated_data):
        user = User(
                email=validated_data["email"],
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                is_superuser=validated_data["is_superuser"],
                is_staff=validated_data["is_staff"],
            )
        user.set_password(validated_data["password"])

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name',)
        extra_kwargs = {'password':{'write_only': True}}
        ordering = ['id']

    def create(self, validated_data):
        user = User(
                email=validated_data["email"],
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )
        user.set_password(validated_data["password"])

        user.save()

        return user

