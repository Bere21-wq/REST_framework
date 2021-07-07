from django.contrib import admin

from .models import Detalles
from .models import Director
from .models import Pelicula

admin.site.register(Pelicula)
admin.site.register(Director)
admin.site.register(Detalles)
