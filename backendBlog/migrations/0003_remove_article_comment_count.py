# Generated by Django 3.0.3 on 2020-03-01 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendBlog', '0002_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='comment_count',
        ),
    ]
