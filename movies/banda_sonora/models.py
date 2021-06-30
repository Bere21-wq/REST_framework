from django.db import models

class Musica(models.Model):
    METAL = 'Metal'
    ROCK = 'Rock'
    CLASICA = 'Clasica'
    SALSA = 'Salsa'
    POP = 'Pop'
    GENRE = [[METAL,'METAL'],[ROCK,'ROCK'],[CLASICA,'CLASICA'],[SALSA,'SALSA'],[POP,'POP']]

    cancion = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    año = models.DateField()
    genero = models.CharField(max_length=100, choices=GENRE)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cancion
