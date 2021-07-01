from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from banda_sonora.models import Musica

class TestMusicaView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
       
        cls.musica1 = Musica.objects.create(cancion='cancion test 1', artista='artista test 1', año='2021-06-16', genero='Metal', owner=test_user1)
        cls.musica2 = Musica.objects.create(cancion='cancion test 2', artista='artista test 2', año='2021-06-16', genero='Metal', owner=test_user1)
        
        cls.response = reverse('musica:index') 
        cls.client = APIClient()

    def test_listado(self):
        """
        Prueba si cualquier usuario (con o sin autenticacion)
        puede ver el listado de banda sonora.
        """
        respuesta = self.client.get(self.response)
        self.assertEqual(200, respuesta.status_code)
        print(self.response)
        print(respuesta.data)
        
    def test_numero_elementos_BD(self):
        """
        Prueba si el numero de elementos en lista coincide 
        con el numero de elementos en base de datos.
        """
        respuesta         = self.client.get(self.response)
        num_elementos     = Musica.objects.count()
        self.assertEqual(num_elementos, len(respuesta.data))

    # def test_match_elementos_BD(self):
    #     """
    #     Prueba que cada elemento de la lista coincide con 
    #     un elemento en la base de datos.
    #     """
    #     respuesta = self.client.get(self.response)
    #     print(respuesta.data)
    #     objeto_1 = Musica.objects.filter(cancion__contains=respuesta.data[0]['cancion'], artista__contains=respuesta.data[0]['artista'])
    #     objeto_2 = Musica.objects.filter(cancion__contains=respuesta.data[1]['cancion'], artista__contains=respuesta.data[1]['artista'])
        
    #     if objeto_1.exists and objeto_2.exists:
    #         print('Los registros estan en la base de datos')
    #     else:
    #         pass

    def test_recupera_un_solo_elemento(self):
         """
         Prueba si se recupera solo uno de los registros de la lista
         """
         self.detalle = reverse('musica:detail', kwargs={'pk' : self.musica1.id})
         respuesta = self.client.get(self.detalle)
         self.assertEqual(200, respuesta.status_code)
         self.assertEqual(respuesta.data, {'id': 1, 'owner': 'testuser1', 'cancion': 'cancion test 1', 'artista': 'artista test 1', 'año': '2021-06-16', 'genero': 'Metal'})
 
    def test_crear_POST_con_autenticacion(self):
        """
        Prueba si un usuario loggeado puede crear un registro de banda sonora.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data_info = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta = self.client.post(self.response, data_info)
        print(respuesta.data)      
        self.assertEqual(201, respuesta.status_code)
        
    def test_crear_POST_sin_autenticacion(self):
        """
        Prueba si un usuario NO AUTORIZADO puede crear un registro de banda sonora.
        """
        data_info = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta = self.client.post(self.response, data_info)
        print(respuesta.data)      
        self.assertEqual(401, respuesta.status_code)
    

    def test_num_elementos_POST(self):
        """
        Prueba si el numero de elementos 'n' en la lista aumenta 
        a 'n+1' después de crear un registro.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        respuesta_pre_post     = self.client.get(self.response)
        data_info              = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta_post         = self.client.post(self.response, data_info)
        num_elementos_pos_post = Musica.objects.count()
        self.assertEqual(num_elementos_pos_post, len(respuesta_pre_post.data)+1)

    def test_post_list(self):
        """
        Comprueba si un registro recién creado aparece en 
        el listado general y la informacion coincide.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data_info      = {
                         'cancion': 'cancion que deberia estar incluida en mi lista', 
                         'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'
                         }
        respuesta_post = self.client.post(self.response, data_info)   
        respuesta_get  = self.client.get(self.response)
        comprobacion_post = Musica.objects.filter(cancion__contains='cancion que deberia estar incluida en mi lista')
        if comprobacion_post.exists():
            print(comprobacion_post)
            print ("El registro nuevo aparece en la lista")
        self.assertEqual(respuesta_get.data[2], respuesta_post.data)
