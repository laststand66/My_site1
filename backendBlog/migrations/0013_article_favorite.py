# Generated by Django 3.0.3 on 2020-03-10 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendBlog', '0012_article_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorited', to=settings.AUTH_USER_MODEL),
        ),
    ]