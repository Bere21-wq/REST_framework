# Generated by Django 3.2.4 on 2021-06-28 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Musica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancion', models.CharField(max_length=200)),
                ('artista', models.CharField(max_length=200)),
                ('año', models.DateField()),
                ('genero', models.CharField(choices=[['Metal', 'METAL'], ['Rock', 'ROCK'], ['Clasica', 'CLASICA'], ['Salsa', 'SALSA'], ['Pop', 'POP']], max_length=100)),
            ],
        ),
    ]
