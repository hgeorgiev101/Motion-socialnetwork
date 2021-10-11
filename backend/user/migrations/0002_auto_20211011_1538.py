# Generated by Django 3.2.7 on 2021-10-11 13:38

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='things_user_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_things', to='interest.Interest'),
        ),
    ]
