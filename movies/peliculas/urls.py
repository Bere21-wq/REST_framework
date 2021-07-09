from django.urls import path

from peliculas.views import PeliculaViewSet
from peliculas.views import UserDetail
from peliculas.views import UserList

app_name = "pelicula"
pelicula_list = PeliculaViewSet.as_view({"get": "list", "post": "create"})
pelicula_detail = PeliculaViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = [
    path("", pelicula_list, name="index"),
    path("<int:pk>/", pelicula_detail, name="detail"),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
