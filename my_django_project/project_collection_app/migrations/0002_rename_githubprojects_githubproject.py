# Generated by Django 4.0.3 on 2022-03-27 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_collection_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GithubProjects',
            new_name='GithubProject',
        ),
    ]
