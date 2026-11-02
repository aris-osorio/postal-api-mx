from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, filters
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
    CodigoPostalDetailSerializer,
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']


class CatMunicipioViewSet(SoftDeleteModelViewSet):
    queryset = CatMunicipio.objects.all().order_by('id')
    serializer_class = CatMunicipioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']
    filterset_fields = ['estado_id']


class CatCiudadViewSet(SoftDeleteModelViewSet):
    queryset = CatCiudad.objects.all().order_by('id')
    serializer_class = CatCiudadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    filterset_fields = ['estado_id']


class CatTipoAsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = CatTipoAsentamiento.objects.all().order_by('id')
    serializer_class = CatTipoAsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']


class CatZonaAsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = CatZonaAsentamiento.objects.all().order_by('id')
    serializer_class = CatZonaAsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


class CodigoPostalViewSet(SoftDeleteModelViewSet):
    queryset = CodigoPostal.objects.all().order_by('id')
    serializer_class = CodigoPostalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['codigo']
    filterset_fields = ['municipio_id', 'ciudad_id']
    

class CodigoPostalDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CodigoPostalDetailSerializer
    
    def get_object(self):
        codigo = self.kwargs.get('codigo')
        
        return get_object_or_404(
            CodigoPostal.objects.filter(deleted_at__isnull=True),
            codigo=codigo
        )


class AsentamientoViewSet(SoftDeleteModelViewSet):
    queryset = Asentamiento.objects.all().order_by('id')
    serializer_class = AsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    filterset_fields = ['codigo_postal_id', 'tipo_asentamiento_id', 'zona_id']