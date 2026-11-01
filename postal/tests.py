from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CatEstado, CatMunicipio, CatCiudad

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