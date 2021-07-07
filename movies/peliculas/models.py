from django.db import models

from banda_sonora.models import Musica


class Director(models.Model):
    director = models.CharField(max_length=200)

    def __str__(self):
        return self.director


class Pelicula(models.Model):
    Terror = "TERROR"
    Comedia = "COMEDIA"
    Drama = "DRAMA"
    Infantil = "INFANTIL"
    Romantica = "ROMANTICA"
    GENRE = [
        [Terror, "TERROR"],
        [Comedia, "COMEDIA"],
        [Drama, "DRAMA"],
        [Infantil, "INFANTIL"],
        [Romantica, "ROMANTICA"],
    ]

    A = "A"
    B = "B"
    C = "C"
    CLASIFICACION = [[A, "A"], [B, "B"], [C, "C"]]

    nombre = models.CharField(max_length=200)
    genero_pelicula = models.CharField(max_length=100, choices=GENRE)
    director_pelicula = models.ForeignKey(Director, on_delete=models.CASCADE)
    clasificacion = models.CharField(max_length=1, choices=CLASIFICACION)
    owner = models.ForeignKey(
        "auth.User", related_name="duenio", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


class Detalles(models.Model):
    """
    Este sera el modelo para la tabla con los construidos de ambas aplicaciones
    """

    nombre = models.ForeignKey(
        Pelicula, on_delete=models.CASCADE, related_name="detalles"
    )
    musica = models.ForeignKey(
        Musica, on_delete=models.CASCADE, related_name="detalles"
    )
    costo = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.nombre}"
