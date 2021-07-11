from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from peliculas.models import Pelicula, Director, Detalles
from banda_sonora.models import Musica

class TestPeliculasView(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        cls.director_prueba_1 = Director.objects.create(director="Director de prueba 1")
        cls.director_prueba_2 = Director.objects.create(director="Director de prueba 2")
        cls.pelicula1 = Pelicula.objects.create(
            nombre="pelicula prueba",
            genero_pelicula="TERROR",
            director_pelicula=cls.director_prueba_1,
            clasificacion="A",
            owner=test_user1,
        )
        cls.banda_sonora_prueba_1 = Musica.objects.create(
                                    cancion="cancion test 1",
                                    artista="artista test 1",
                                    año="2021-06-16",
                                    genero="Metal",
                                    owner=test_user1,
                                    )
        cls.banda_sonora_prueba_2 = Musica.objects.create(
                                    cancion="cancion test 2",
                                    artista="artista test 2",
                                    año="2021-06-16",
                                    genero="Salsa",
                                    owner=test_user1,
                                    )
        cls.detalles_1 = Detalles.objects.create(
                                                nombre = cls.pelicula1,
                                                musica = cls.banda_sonora_prueba_1,
                                                costo = 100,
                                                )
        cls.url_response = reverse("pelicula:index")
        cls.client = APIClient()

    def test_listado_de_peliculas_usuario_loggeado(self):
        """
        Prueba si un usuario loggeado puede ver el listado de peliculas.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        solicitud_get = self.client.get(self.url_response)
        self.assertEqual(200, solicitud_get.status_code)

    def test_listado_de_peliculas_usuario_no_loggeado(self):
        """
        Prueba si un usuario NO AUTORIZADO puede ver el listado.
        """
        solicitud_get = self.client.get(self.url_response)
        self.assertEqual(401, solicitud_get.status_code)

    def test_numero_elementos_en_BD(self):
        """
        Prueba si el numero de elementos en lista coincide
        con el numero de elementos en base de datos.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        solicitud_get = self.client.get(self.url_response)
        num_elementos = Pelicula.objects.count()
        self.assertEqual(num_elementos, len(solicitud_get.data))

    def test_match_elementos_en_BD(self):
        """
        Prueba que cada elemento de la lista coincide con
        un elemento en la base de datos.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        solicitud_get = self.client.get(self.url_response)
        print(solicitud_get.data)
    
        for i in solicitud_get.data:
            pelicula_id = Pelicula.objects.get(id=i["id"])
            self.assertEqual(i["nombre"], pelicula_id.nombre)
            self.assertEqual(i["owner"], pelicula_id.owner.username)
            print(i["representacion_detalles"])
            for j in i["representacion_detalles"]:
                print(j)
                detalles = Detalles.objects.get(id=j["id"])
                print(detalles.id)
                self.assertEqual(detalles.nombre.nombre, j["nombre_representacion_pelicula"])
                self.assertEqual(detalles.musica.cancion, j["representacion_musica"]["cancion"])
                self.assertEqual(str(detalles.costo), j["costo"])

    def test_recupera_un_solo_elemento_de_peliculas(self):
        """
        Prueba si recupera uno solo de los elementos de la base de datos.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        item = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        solicitud_get = self.client.get(item)
        print(solicitud_get.data)
        self.assertEqual(200, solicitud_get.status_code)
        item_en_BD = Pelicula.objects.get(id=solicitud_get.data["id"])
        self.assertEqual(solicitud_get.data["nombre"], item_en_BD.nombre)
        self.assertEqual(solicitud_get.data["direccion"], str(item_en_BD.director_pelicula))
        self.assertEqual(solicitud_get.data["owner"], item_en_BD.owner.username)

        for i in solicitud_get.data["representacion_detalles"]:
            item_detalles_en_BD = Detalles.objects.get(id=i["id"])
            print(item_detalles_en_BD.id)
            self.assertEqual(i["representacion_musica"]["id"], item_detalles_en_BD.musica.id)
            self.assertEqual(i["nombre_representacion_pelicula"], str(item_detalles_en_BD.nombre))
            self.assertEqual(i["costo"], str(item_detalles_en_BD.costo))


    def test_crear_POST_con_autenticacion(self):
        """
        Prueba si un usuario loggeado puede crear un nuevo registro.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        #Iterar sobre la banda_sonora
        data_info = {
                    "banda_sonora": [self.banda_sonora_prueba_1.id],
                    "costo_entrada": 6,
                    "nombre": "pelicula para prueba post",
                    "genero_pelicula": "DRAMA",
                    "director_pelicula": self.director_prueba_1.id,
                    "clasificacion": "C",
                    }
        solicitud_post = self.client.post(self.url_response, data_info)
        print(solicitud_post.data)
        self.assertEqual(201, solicitud_post.status_code)
        
    def test_crear_POST_sin_autenticacion(self):
        """
        Prueba si un usuario NO AUTORIZADO puede crear un registro de peliculas.
        """
        data_info = {
            "banda_sonora": [self.banda_sonora_prueba_1.id],
            "costo_entrada": 6,
            "nombre": "pelicula para prueba post",
            "genero_pelicula": "DRAMA",
            "director_pelicula": self.director_prueba_1.id,
            "clasificacion": "C",
            }
        solicitud_post = self.client.post(self.url_response, data_info)
        self.assertEqual(401, solicitud_post.status_code)

    def test_num_elementos_despues_de_POST(self):
        """
        Prueba si el numero de elementos 'n' en la lista aumenta
        a 'n+1' después de crear un registro.
        """
        #Tambien deben contarse el numero de elementos en tabla Detalles
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        num_elementos_pelicula_pre_post = Pelicula.objects.count()
        num_elementos_detalles_pre_post = Detalles.objects.count()
        data_info = {
            "banda_sonora": [self.banda_sonora_prueba_1.id],
            "costo_entrada": 6,
            "nombre": "pelicula para prueba post",
            "genero_pelicula": "DRAMA",
            "director_pelicula": self.director_prueba_1.id,
            "clasificacion": "C",
            }
        solicitud_post = self.client.post(self.url_response, data_info)
        num_elementos_pelicula_pos_post = Pelicula.objects.count()
        num_elementos_detalle_pos_post = Detalles.objects.count()
        self.assertEqual(num_elementos_pelicula_pos_post, num_elementos_pelicula_pre_post+1)
        self.assertEqual(num_elementos_detalle_pos_post, num_elementos_detalles_pre_post+1)
        self.assertEqual(201, solicitud_post.status_code)
    

    #Corregir el nombre de la funcion.
    #Comparar con la representacion de los detalles, tal como hiciste en la prueba de listado.
    def test_elemento_post_coincide_con_BD(self):
        """
        Comprueba si un registro recién creado aparece en
        el listado de peliculas y la informacion coincide.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        data_info = {
            "banda_sonora": [self.banda_sonora_prueba_1.id],
            "costo_entrada": 6,
            "nombre": "pelicula para prueba post",
            "genero_pelicula": "DRAMA",
            "director_pelicula": self.director_prueba_1.id,
            "clasificacion": "C",
            }
        solicitud_post = self.client.post(self.url_response, data_info)
        consulta_BD = Pelicula.objects.get(id=solicitud_post.data["id"])
        self.assertEqual(data_info["nombre"], consulta_BD.nombre)
        self.assertEqual(data_info["director_pelicula"], consulta_BD.director_pelicula.id)
        self.assertEqual(data_info["clasificacion"], consulta_BD.clasificacion)

        for i in solicitud_post.data["representacion_detalles"]:
            detalles = Detalles.objects.get(id=i["id"])
            self.assertEqual(detalles.nombre.nombre, i["nombre_representacion_pelicula"])
            self.assertEqual(detalles.musica.cancion, i["representacion_musica"]["cancion"])
            self.assertEqual(str(detalles.costo), i["costo"])
            for j in data_info["banda_sonora"]:
                self.assertEqual(detalles.musica.pk, j)

    def test_actualizacion_total_PUT(self):
        """
        Prueba si un usuario loggeado puede actualizar de manera total
        un registro.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        info_original = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        data_info = {
                    "banda_sonora": [self.banda_sonora_prueba_2.id],
                    "costo_entrada": 50,
                    "nombre": "pelicula para prueba PUT",
                    "genero_pelicula": "DRAMA",
                    "director_pelicula": self.director_prueba_2.id,
                    "clasificacion": "B",
                    }
        solicitud_actualizacion = self.client.put(info_original, data_info)
        self.assertEqual(200, solicitud_actualizacion.status_code)

    def test_num_elementos_peliculas_despues_actualizacion_PUT(self):
        """
        Prueba si el numero de elementos en base de datos de peliculas
        permanece constante tras haber realizado la actualizacion PUT.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        info_original = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        num_elementos_peliculas_pre_put = Pelicula.objects.count()
        data_info = {
                    "banda_sonora": [self.banda_sonora_prueba_2.id],
                    "costo_entrada": 50,
                    "nombre": "pelicula para prueba PUT",
                    "genero_pelicula": "DRAMA",
                    "director_pelicula": self.director_prueba_2.id,
                    "clasificacion": "B",
                    }
        solicitud_actualizacion = self.client.put(info_original, data_info)
        num_elementos_peliculas_pos_put = Pelicula.objects.count()
        self.assertEqual(num_elementos_peliculas_pos_put, num_elementos_peliculas_pre_put)

    def test_num_elementos_detalles_despues_actualizacion_PUT(self):
        """
        Prueba que el numero de elementos en la relacion Detalles aumenta si en 
        la actualizacion se agrega mas de una banda sonora para una misma pelicula.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        info_original = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        data_info = {
                    "banda_sonora": [self.banda_sonora_prueba_1.id, self.banda_sonora_prueba_2.id],
                    "costo_entrada": 50,
                    "nombre": "pelicula para prueba PUT",
                    "genero_pelicula": "DRAMA",
                    "director_pelicula": self.director_prueba_2.id,
                    "clasificacion": "B",
                    }
        num_elementos_detalles_pre_put = Detalles.objects.count()
        solicitud_actualizacion = self.client.put(info_original, data_info)
        num_elementos_detalles_pos_put = Detalles.objects.count()
        self.assertEqual(len(data_info["banda_sonora"]), num_elementos_detalles_pos_put)

    def test_elemento_put_coincide_con_BD(self):
        """
        Prueba si un elemento completamente actualizado coincide con 
        un elemento en base de datos.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        info_original = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        num_elementos_peliculas_pre_put = Pelicula.objects.count()
        num_elementos_detalles_pre_put = Detalles.objects.count()
        data_info = {
                    "banda_sonora": [self.banda_sonora_prueba_1.id],
                    "costo_entrada": 50,
                    "nombre": "pelicula para prueba PUT",
                    "genero_pelicula": "DRAMA",
                    "director_pelicula": self.director_prueba_2.id,
                    "clasificacion": "B",
                    }
        solicitud_actualizacion = self.client.put(info_original, data_info)
        item_actualizado = Pelicula.objects.get(id=solicitud_actualizacion.data["id"])
        self.assertEqual(solicitud_actualizacion.data["nombre"], item_actualizado.nombre)
        self.assertEqual(solicitud_actualizacion.data["direccion"], str(item_actualizado.director_pelicula))

        for i in solicitud_actualizacion.data["representacion_detalles"]:
            detalles = Detalles.objects.get(id=i["id"])
            self.assertEqual(detalles.nombre.nombre, i["nombre_representacion_pelicula"])
            self.assertEqual(detalles.musica.cancion, i["representacion_musica"]["cancion"])
            self.assertEqual(str(detalles.costo), i["costo"])
            for j in data_info["banda_sonora"]:
                self.assertEqual(detalles.musica.pk, j)

    def test_actualizacion_parcial_PATCH(self):
        """
        Prueba si un usuario loggeado puede modificar parcialmente
        un registro y este coincide con un elemento en base de datos.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        info_original = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        data_info = {
            "banda_sonora": [self.banda_sonora_prueba_1.id],
            "costo_entrada": 6,
            "nombre": "pelicula para prueba PATCH",
            "genero_pelicula": "TERROR",
            "director_pelicula": self.director_prueba_1.id,
            "clasificacion": "A",
            }
        solicitud_actualicacion_parcial = self.client.patch(info_original, data_info)
        print(solicitud_actualicacion_parcial.data)
        self.assertEqual(200, solicitud_actualicacion_parcial.status_code)
        item_pelicula_actualizado = Pelicula.objects.get(id=solicitud_actualicacion_parcial.data["id"])
        self.assertEqual(solicitud_actualicacion_parcial.data["nombre"], item_pelicula_actualizado.nombre)
        
        for i in solicitud_actualicacion_parcial.data["representacion_detalles"]:
            item_detalle_actualizado = Detalles.objects.get(id=i["id"])
            self.assertEqual(i["nombre_representacion_pelicula"], item_detalle_actualizado.nombre.nombre)
            self.assertEqual(i["representacion_musica"]["cancion"], item_detalle_actualizado.musica.cancion)
            self.assertEqual(i["costo"], str(item_detalle_actualizado.costo))
            for j in data_info["banda_sonora"]:
                self.assertEqual(item_detalle_actualizado.musica.pk, j)

    def test_DELETE(self):
        """
        Prueba si el numero de registros en base de datos disminuye 
        al eliminar un registro de peliculas.
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        item_a_eliminar = reverse("pelicula:detail", kwargs={"pk": self.pelicula1.id})
        num_registros_peliculas_pre_delete = Pelicula.objects.count()
        num_registros_detalles_pre_delete = Detalles.objects.count()
        solicitud_delete = self.client.delete(item_a_eliminar)
        num_registros_peliculas_pos_delete = Pelicula.objects.count()
        num_registros_detalles_pos_delete = Detalles.objects.count()
        self.assertEqual(num_registros_peliculas_pre_delete-1, num_registros_peliculas_pos_delete)
        self.assertEqual(num_registros_detalles_pre_delete-1, num_registros_detalles_pos_delete)
        self.assertEqual(204, solicitud_delete.status_code)
        registro_eliminado = Pelicula.objects.filter(pk=self.pelicula1.id).exists()
        self.assertFalse(registro_eliminado)
        
