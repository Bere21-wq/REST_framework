from django.urls import path
from banda_sonora.views import MusicaListView

app_name = 'musica'

urlpatterns = [
    path('',MusicaListView.as_view(), name='musica')
]