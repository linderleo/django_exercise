# Generated by Django 4.0.3 on 2022-03-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_collection_app', '0003_githubproject_created_githubproject_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubproject',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]