from peliculas.models import Detalles, Pelicula
from banda_sonora.models import Musica

prueba = Pelicula.objects.get(id=100)
print(prueba)
musica = Musica.objects.get(id=3)
print(musica)
Detalles(nombre=prueba, musica=musica , costo=0)

