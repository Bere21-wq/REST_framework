from django.urls import path
from peliculas.views import PeliculaViewSet, DirectorViewSet, DetallesViewSet

app_name = 'pelicula'
pelicula_list = PeliculaViewSet.as_view({'get': 'list', 'post': 'create'})
pelicula_detail = PeliculaViewSet.as_view({
    'get':'retrieve', 
    'put':'update', 
    'patch': 'partial_update',
    'delete': 'destroy',
})



urlpatterns = [
    path('', pelicula_list),
    path('<int:pk>/', pelicula_detail),
]