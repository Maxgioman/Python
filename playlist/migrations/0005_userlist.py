# Generated by Django 2.2.7 on 2019-11-19 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0004_delete_userlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserList',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playlist.User')),
            ],
            bases=('playlist.user',),
        ),
    ]
