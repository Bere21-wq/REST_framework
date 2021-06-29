from django.urls import path
from banda_sonora.views import MusicaViewSet, UserList, UserDetail

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
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]