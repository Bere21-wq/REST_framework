from django.urls import path

from banda_sonora.views import MusicaViewSet
from banda_sonora.views import UserDetail
from banda_sonora.views import UserList

app_name = "musica"
musica_list = MusicaViewSet.as_view({"get": "list", "post": "create"})
musica_detail = MusicaViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("", musica_list, name="index"),
    path("<int:pk>", musica_detail, name="detail"),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
