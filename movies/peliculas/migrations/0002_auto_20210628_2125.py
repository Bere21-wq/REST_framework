# Generated by Django 3.2.4 on 2021-06-28 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='director',
            name='highlighted',
        ),
        migrations.RemoveField(
            model_name='director',
            name='owner',
        ),
    ]
