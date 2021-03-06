# Generated by Django 3.2.9 on 2022-06-20 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getchords', '0002_auto_20211226_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(default=None, upload_to='')),
                ('chords', models.TextField(default='')),
            ],
            options={
                'db_table': 'song_chords_lite',
            },
        ),
        migrations.AlterField(
            model_name='songchords',
            name='song_chord_type',
            field=models.CharField(default='', max_length=20),
        ),
    ]
