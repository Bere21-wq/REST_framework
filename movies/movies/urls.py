"""movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from peliculas.views import DetallesViewSet, DirectorViewSet

detalles_list = DetallesViewSet.as_view({'get': 'list', 'post': 'create'})
detalles_detail = DetallesViewSet.as_view({
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



urlpatterns = [
    path('banda_sonora/', include('banda_sonora.urls')),
    path('peliculas/', include('peliculas.urls')),
    path('detalles/', detalles_list),
    path('detalles/<int:pk>/', detalles_detail),
    path('directores/', director_list),
    path('directores/<int:pk>/', director_detail),
    path('admin/', admin.site.urls),
]
