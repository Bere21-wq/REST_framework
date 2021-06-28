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

director_list = DirectorViewSet.as_view({'get': 'list', 'post': 'create'})
director_detail = DirectorViewSet.as_view({
    'get':'retrieve', 
    'put':'update', 
    'patch': 'partial_update',
    'delete': 'destroy',
})

detalles_list = DetallesViewSet.as_view({'get': 'list', 'post': 'create'})
detalles_detail = DetallesViewSet.as_view({
    'get':'retrieve', 
    'put':'update', 
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', pelicula_list),
    path('<int:pk>/', pelicula_detail),
    path('director/', director_list),
    path('director/<int:pk>/', director_detail),
]