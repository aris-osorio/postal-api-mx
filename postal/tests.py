from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CatEstado, CatMunicipio, CatCiudad, CodigoPostal, CatTipoAsentamiento, CatZonaAsentamiento

User = get_user_model()

class CatEstadoTestCase(APITestCase):
    """
    Test suite for validating CatEstado API endpoints, 
    authentication barriers, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.estado = CatEstado.objects.create(clave='01', nombre='Aguascalientes')
        self.url_list = '/api/v1/estados/'
        self.url_detail = f'/api/v1/estados/{self.estado.id}/'
    
    def test_create_cat_estado_success(self):
        """Ensure an authenticated user can successfully create a new state."""
        data = {'clave': '02', 'nombre': 'Baja California'}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatEstado.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Baja California')
    
    def test_create_cat_estado_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'clave': ''}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_cat_estado_detail(self):
        """Ensure a single state can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.estado.nombre)
    
    def test_list_cat_estados(self):
        """Ensure the endpoint returns the list of active states."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Aguascalientes')

    def test_update_cat_estado_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'nombre': 'Aguascalientes Updated'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estado.refresh_from_db()
        self.assertEqual(self.estado.nombre, 'Aguascalientes Updated')

    def test_search_cat_estados(self):
        """Ensure search fields filter results correctly by name or code."""
        CatEstado.objects.create(clave='03', nombre='Jalisco')
        
        response = self.client.get(f"{self.url_list}?search=Jalisco")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Jalisco')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.estado.refresh_from_db()
        self.assertIsNotNone(self.estado.deleted_at)

        self.assertEqual(CatEstado.objects.count(), 0)

        self.assertEqual(CatEstado.all_objects.count(), 1)
            

    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)


class CatMunicipioTestCase(APITestCase):
    """
    Test suite for validating CatMunicipio API endpoints, 
    authentication barriers, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.estado = CatEstado.objects.create(clave='01', nombre='Aguascalientes')
        self.municipio = CatMunicipio.objects.create(
            clave='001', 
            nombre='Aguascalientes', 
            estado_id=self.estado
        )
        
        self.url_list = '/api/v1/municipios/'
        self.url_detail = f'/api/v1/municipios/{self.municipio.id}/'
    
    def test_create_cat_municipio_success(self):
        """Ensure an authenticated user can successfully create a new municipality."""
        data = {
            'clave': '002', 
            'nombre': 'Calvillo', 
            'estado_id': self.estado.id
        }
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatMunicipio.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Calvillo')
    
    def test_create_cat_municipio_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'clave': '', 'estado_id': self.estado.id}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_cat_municipio_detail(self):
        """Ensure a single municipality can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.municipio.nombre)
    
    def test_list_cat_municipios(self):
        """Ensure the endpoint returns the list of active municipalities."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Aguascalientes')

    def test_update_cat_municipio_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'nombre': 'Aguascalientes Updated'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.municipio.refresh_from_db()
        self.assertEqual(self.municipio.nombre, 'Aguascalientes Updated')

    def test_search_cat_municipios(self):
        """Ensure search fields filter results correctly by name or code."""
        CatMunicipio.objects.create(clave='002', nombre='Calvillo', estado_id=self.estado)
        
        response = self.client.get(f"{self.url_list}?search=Calvillo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Calvillo')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.municipio.refresh_from_db()
        self.assertIsNotNone(self.municipio.deleted_at)

        self.assertEqual(CatMunicipio.objects.count(), 0)

        self.assertEqual(CatMunicipio.all_objects.count(), 1)
            

    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)
        
        
class CatCiudadTestCase(APITestCase):
    """
    Test suite for validating CatCiudad API endpoints, 
    authentication barriers, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data, parent hierarchy, and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.estado = CatEstado.objects.create(clave='01', nombre='Aguascalientes')
        
        self.ciudad = CatCiudad.objects.create(
            clave='01', 
            nombre='Aguascalientes', 
            estado_id=self.estado
        )
        
        self.url_list = '/api/v1/ciudades/'
        self.url_detail = f'/api/v1/ciudades/{self.ciudad.id}/'
    
    def test_create_cat_ciudad_success(self):
        """Ensure an authenticated user can successfully create a new city."""
        data = {
            'clave': '03', 
            'nombre': 'San Francisco de los Romo', 
            'estado_id': self.estado.id
        }
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatCiudad.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'San Francisco de los Romo')
    
    def test_create_cat_ciudad_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'clave': '', 'estado_id': self.estado.id}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_cat_ciudad_detail(self):
        """Ensure a single city can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.ciudad.nombre)
    
    def test_list_cat_ciudades(self):
        """Ensure the endpoint returns the list of active cities."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Aguascalientes')

    def test_update_cat_ciudad_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'nombre': 'Aguascalientes Updated'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ciudad.refresh_from_db()
        self.assertEqual(self.ciudad.nombre, 'Aguascalientes Updated')

    def test_search_cat_ciudades(self):
        """Ensure search fields filter results correctly by name or code."""
        CatCiudad.objects.create(clave='03', nombre='San Francisco de los Romo', estado_id=self.estado)
        
        response = self.client.get(f"{self.url_list}?search=San Francisco de los Romo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'San Francisco de los Romo')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.ciudad.refresh_from_db()
        self.assertIsNotNone(self.ciudad.deleted_at)

        self.assertEqual(CatCiudad.objects.count(), 0)

        self.assertEqual(CatCiudad.all_objects.count(), 1)
            
    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)
        
        
class CodigoPostalTestCase(APITestCase):
    """
    Test suite for validating CodigoPostal API endpoints, 
    foreign key dependencies, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data, hierarchical dependencies, and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.estado = CatEstado.objects.create(clave='01', nombre='Aguascalientes')
        self.municipio = CatMunicipio.objects.create(clave='001', nombre='Aguascalientes', estado_id=self.estado)
        self.ciudad = CatCiudad.objects.create(clave='01', nombre='Aguascalientes', estado_id=self.estado)
        
        self.codigo_postal = CodigoPostal.objects.create(
            codigo='20000',
            municipio_id=self.municipio,
            ciudad_id=self.ciudad
        )
        
        self.url_list = '/api/v1/codigos-postales/'
        self.url_detail = f'/api/v1/codigos-postales/{self.codigo_postal.id}/'
    
    def test_create_codigo_postal_success(self):
        """Ensure an authenticated user can successfully create a new postal code."""
        data = {
            'codigo': '20001',
            'municipio_id': self.municipio.id,
            'ciudad_id': self.ciudad.id
        }
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CodigoPostal.objects.count(), 2)
        self.assertEqual(response.data['codigo'], '20001')
    
    def test_create_codigo_postal_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'codigo': '', 'municipio_id': self.municipio.id}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_codigo_postal_detail(self):
        """Ensure a single postal code can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo'], self.codigo_postal.codigo)
    
    def test_list_codigos_postales(self):
        """Ensure the endpoint returns the list of active postal codes."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['codigo'], '20000')

    def test_update_codigo_postal_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'codigo': '20999'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.codigo_postal.refresh_from_db()
        self.assertEqual(self.codigo_postal.codigo, '20999')

    def test_search_codigos_postales(self):
        """Ensure search fields filter results correctly by postal code."""
        CodigoPostal.objects.create(codigo='20100', municipio_id=self.municipio)
        
        response = self.client.get(f"{self.url_list}?search=20100")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['codigo'], '20100')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.codigo_postal.refresh_from_db()
        self.assertIsNotNone(self.codigo_postal.deleted_at)

        self.assertEqual(CodigoPostal.objects.count(), 0)

        self.assertEqual(CodigoPostal.all_objects.count(), 1)
            
    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)
        
        
class CatTipoAsentamientoTestCase(APITestCase):
    """
    Test suite for validating CatTipoAsentamiento API endpoints, 
    authentication barriers, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.tipo_asentamiento = CatTipoAsentamiento.objects.create(
            clave='01', 
            nombre='Colonia'
        )
        
        self.url_list = '/api/v1/tipos-asentamiento/'
        self.url_detail = f'/api/v1/tipos-asentamiento/{self.tipo_asentamiento.id}/'
    
    def test_create_cat_tipo_asentamiento_success(self):
        """Ensure an authenticated user can successfully create a new settlement type."""
        data = {
            'clave': '02', 
            'nombre': 'Ejido'
        }
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatTipoAsentamiento.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Ejido')
    
    def test_create_cat_tipo_asentamiento_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'clave': '', 'nombre': ''}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_cat_tipo_asentamiento_detail(self):
        """Ensure a single settlement type can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.tipo_asentamiento.nombre)
    
    def test_list_cat_tipos_asentamiento(self):
        """Ensure the endpoint returns the list of active settlement types."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Colonia')

    def test_update_cat_tipo_asentamiento_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'nombre': 'Colonia Updated'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo_asentamiento.refresh_from_db()
        self.assertEqual(self.tipo_asentamiento.nombre, 'Colonia Updated')

    def test_search_cat_tipos_asentamiento(self):
        """Ensure search fields filter results correctly by name or code."""
        CatTipoAsentamiento.objects.create(clave='02', nombre='Ejido')
        
        response = self.client.get(f"{self.url_list}?search=Ejido")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Ejido')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.tipo_asentamiento.refresh_from_db()
        self.assertIsNotNone(self.tipo_asentamiento.deleted_at)

        self.assertEqual(CatTipoAsentamiento.objects.count(), 0)

        self.assertEqual(CatTipoAsentamiento.all_objects.count(), 1)
            
    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)
        
        
class CatZonaAsentamientoTestCase(APITestCase):
    """
    Test suite for validating CatZonaAsentamiento API endpoints, 
    authentication barriers, and soft-delete business logic.
    """
    
    def setUp(self):
        """Configure test data and authentication credentials before each test."""
        self.user = User.objects.create_user(username='test_user', password='securepassword123')
        self.client.force_authenticate(user=self.user)
        
        self.zona_asentamiento = CatZonaAsentamiento.objects.create(
            nombre='Urbano'
        )
        
        self.url_list = '/api/v1/zonas-asentamiento/'
        self.url_detail = f'/api/v1/zonas-asentamiento/{self.zona_asentamiento.id}/'
    
    def test_create_cat_zona_asentamiento_success(self):
        """Ensure an authenticated user can successfully create a new settlement zone."""
        data = {
            'nombre': 'Rural'
        }
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CatZonaAsentamiento.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Rural')
    
    def test_create_cat_zona_asentamiento_invalid_data(self):
        """Ensure validation fails when required fields are missing."""
        data = {'nombre': ''}
        response = self.client.post(self.url_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_cat_zona_asentamiento_detail(self):
        """Ensure a single settlement zone can be retrieved by its ID."""
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.zona_asentamiento.nombre)
    
    def test_list_cat_zonas_asentamiento(self):
        """Ensure the endpoint returns the list of active settlement zones."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Urbano')

    def test_update_cat_zona_asentamiento_patch(self):
        """Ensure partial updates (PATCH) modify the record correctly."""
        data = {'nombre': 'Urbano Updated'}
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.zona_asentamiento.refresh_from_db()
        self.assertEqual(self.zona_asentamiento.nombre, 'Urbano Updated')

    def test_search_cat_zonas_asentamiento(self):
        """Ensure search fields filter results correctly by name."""
        CatZonaAsentamiento.objects.create(nombre='Rural')
        
        response = self.client.get(f"{self.url_list}?search=Rural")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Rural')
    
    def test_soft_delete_operation(self):
        """Ensure that a DELETE request performs a soft delete and hides the record from active queries."""
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.zona_asentamiento.refresh_from_db()
        self.assertIsNotNone(self.zona_asentamiento.deleted_at)

        self.assertEqual(CatZonaAsentamiento.objects.count(), 0)

        self.assertEqual(CatZonaAsentamiento.all_objects.count(), 1)
            
    def test_soft_deleted_record_is_hidden_from_list(self):
        """Ensure that soft-deleted records do not appear in list queries."""
        self.client.delete(self.url_detail)
        
        response = self.client.get(self.url_list)
        results = response.data.get('results', response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)