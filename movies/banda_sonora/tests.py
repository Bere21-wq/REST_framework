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
        # print(self.response)
        # print(respuesta.data)
        
    def test_numero_elementos_BD(self):
        """
        Prueba si el numero de elementos en lista coincide 
        con el numero de elementos en base de datos.
        """
        respuesta         = self.client.get(self.response)
        num_elementos     = Musica.objects.count()
        self.assertEqual(num_elementos, len(respuesta.data))

    def test_match_elementos_BD(self):
        """
        Prueba que cada elemento de la lista coincide con 
        un elemento en la base de datos.
        """
        respuesta = self.client.get(self.response)

        for i in respuesta.data:
            #print(i)
            v = Musica.objects.get(id=i['id'])
            self.assertEqual(i['artista'], v.artista)
            self.assertEqual(i['owner'], v.owner.username)
            #print(Musica.objects.filter(id=i['id']).count())

    def test_recupera_un_solo_elemento(self):
         """
         Prueba si se recupera solo uno de los registros de la lista
         """
         detalle = reverse('musica:detail', kwargs={'pk' : self.musica1.id})
         respuesta = self.client.get(detalle)
         #print(respuesta.data['id'])
         self.assertEqual(200, respuesta.status_code)
         valor_consulta = Musica.objects.get(id=respuesta.data['id'])
         #print(valor_consulta)
         self.assertEqual(respuesta.data['cancion'], valor_consulta.cancion)
         self.assertEqual(respuesta.data['artista'], valor_consulta.artista)
         self.assertEqual(respuesta.data['año'], str(valor_consulta.año))

    def test_crear_POST_con_autenticacion(self):
        """
        Prueba si un usuario loggeado puede crear un registro de banda sonora.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data_info = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta = self.client.post(self.response, data_info)
        #print(respuesta.data)      
        self.assertEqual(201, respuesta.status_code)
        
    def test_crear_POST_sin_autenticacion(self):
        """
        Prueba si un usuario NO AUTORIZADO puede crear un registro de banda sonora.
        """
        data_info = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta = self.client.post(self.response, data_info)
        #print(respuesta.data)      
        self.assertEqual(401, respuesta.status_code)
    

    def test_num_elementos_POST(self):
        """
        Prueba si el numero de elementos 'n' en la lista aumenta 
        a 'n+1' después de crear un registro.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        respuesta_pre_post     = Musica.objects.count()
        data_info              = {'cancion': 'cancion test', 'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'}
        respuesta_post         = self.client.post(self.response, data_info)
        num_elementos_pos_post = Musica.objects.count()
        self.assertEqual(num_elementos_pos_post, respuesta_pre_post + 1)

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
        # print(respuesta_post.data['id']) 
        valor_consulta = Musica.objects.get(id=respuesta_post.data['id'])
        self.assertEqual(data_info['cancion'], valor_consulta.cancion)
        self.assertEqual(data_info['artista'], valor_consulta.artista)
        self.assertEqual(data_info['año'], str(valor_consulta.año))
    
    def test_PUT_success(self):
        """
        Prueba si el usuario loggeado puede actualizar TOTALMENTE
        un registro.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        actualizacion = reverse('musica:detail', kwargs={'pk' : self.musica1.id})
        data_info= {
                    'cancion': 'cancion que deberia estar incluida en mi lista', 
                    'artista':'artista test', 'año':'2021-06-16', 'genero':'Metal'
                    }
        respuesta_actualizada = self.client.put(actualizacion, data_info)
        print(respuesta_actualizada.data)
        self.assertEqual(200, respuesta_actualizada.status_code)
        valor_consulta = Musica.objects.get(id=respuesta_actualizada.data['id'])
        #print(valor_consulta)
        self.assertEqual(respuesta_actualizada.data['cancion'], valor_consulta.cancion)
        self.assertEqual(respuesta_actualizada.data['artista'], valor_consulta.artista)
        self.assertEqual(respuesta_actualizada.data['año'], str(valor_consulta.año))

    def test_PATCH_success(self):
        """
        Prueba si el usuario loggeado puede actualizar PARCIALMENTE 
        un registro.
        """
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        actualizacion = reverse('musica:detail', kwargs={'pk' : self.musica1.id})
        data_info= {
                    'cancion': 'cancion que deberia estar incluida en mi lista'
                    }
        respuesta_actualizada = self.client.patch(actualizacion, data_info)
        self.assertEqual(200, respuesta_actualizada.status_code)
        resultado = Musica.objects.get(id=respuesta_actualizada.data['id'])
        self.assertEqual(respuesta_actualizada.data['cancion'], resultado.cancion)

    def test_DELETE(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        url_delete = reverse('musica:detail', kwargs={'pk' : self.musica1.id})
        num_regitros_pre_delete = Musica.objects.all().count()
        respuesta_delete = self.client.delete(url_delete)
        print(respuesta_delete.data)
        num_regitros_actual = Musica.objects.all().count()
        self.assertEqual(204, respuesta_delete.status_code)
        self.assertEqual(num_regitros_pre_delete - 1, num_regitros_actual)

        recuperar_registro = Musica.objects.filter(pk=self.musica1.id).exists()
        self.assertFalse(recuperar_registro)
        print(recuperar_registro)

