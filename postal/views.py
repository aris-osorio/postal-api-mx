from django.utils import timezone
from rest_framework import viewsets
from .models import (
    CatEstado,
    CatMunicipio,
    CatCiudad,
    CatTipoAsentamiento,
    CatZonaAsentamiento,
    CodigoPostal,
    Asentamiento,
)
from .serializers import (
    CatEstadoSerializer,
    CatMunicipioSerializer,
    CatCiudadSerializer,
    CatTipoAsentamientoSerializer,
    CatZonaAsentamientoSerializer,
    CodigoPostalSerializer,
    AsentamientoSerializer,
)


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that intercepts the DELETE request to perform 
    a soft delete instead of deleting the record from the DB.
    """
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


class CatEstadoViewSet(SoftDeleteModelViewSet):
    queryset = CatEstado.objects.all().order_by('id')
    serializer_class = CatEstadoSerializer
    search_fields = ['nombre', 'clave']


class CatMunicipioViewSet(SoftDeleteModelViewSet):
    queryset = CatMunicipio.objects.all().order_by('id')
    serializer_class = CatMunicipioSerializer
    search_fields = ['nombre', 'clave']
    filterset_fields = ['estado_id']


class CatCiudadViewSet(SoftDeleteModelViewSet):
    queryset = CatCiudad.objects.all().order_by('id')
    serializer_class = CatCiudadSerializer
    search_fields = ['nombre']
    filterset_fields = ['estado_id']


class CatTipoAsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = CatTipoAsentamiento.objects.all().order_by('id')
    serializer_class = CatTipoAsentamientoSerializer
    search_fields = ['nombre', 'clave']


class CatZonaAsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = CatZonaAsentamiento.objects.all().order_by('id')
    serializer_class = CatZonaAsentamientoSerializer
    search_fields = ['nombre']


class CodigoPostalViewSet(SoftDeleteModelViewSet):
    queryset = CodigoPostal.objects.all().order_by('id')
    serializer_class = CodigoPostalSerializer
    search_fields = ['codigo']
    filterset_fields = ['municipio_id', 'ciudad_id']


class AsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = Asentamiento.objects.all().order_by('id')
    serializer_class = AsentamientoSerializer
    search_fields = ['nombre']
    filterset_fields = ['codigo_postal_id', 'tipo_asentamiento_id', 'zona_id']