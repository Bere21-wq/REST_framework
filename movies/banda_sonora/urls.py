from django.urls import path
from banda_sonora.views import MusicaViewSet

app_name = 'musica'
musica_list = MusicaViewSet.as_view({'get': 'list', 'post': 'create'})
musica_detail = MusicaViewSet.as_view({
    'get':'retrieve', 
    'put':'update', 
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', musica_list),
    path('<int:pk>', musica_detail),
]