# Generated by Django 2.2.7 on 2019-11-19 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0006_auto_20191119_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersLists',
            fields=[
                ('playlist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playlist.Playlist')),
            ],
            bases=('playlist.playlist',),
        ),
    ]