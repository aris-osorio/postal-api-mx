from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets, filters
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
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


def crud_schema(tag, singular, plural, list_description):
    """
    Genera la documentación de cada operación del ViewSet para que cada
    endpoint (GET, POST, PUT, PATCH, DELETE) tenga su propio título y descripción.

    - tag: grupo en la documentación (ej. 'Municipios')
    - singular: recurso con artículo (ej. 'un municipio')
    - plural: recurso en plural (ej. 'municipios')
    - list_description: texto del listado (búsqueda y filtros)
    """
    return extend_schema_view(
        list=extend_schema(
            tags=[tag],
            summary=f'Listar {plural}',
            description=list_description,
        ),
        retrieve=extend_schema(
            tags=[tag],
            summary=f'Obtener {singular}',
            description=f'Devuelve el detalle de {singular} a partir de su `id`.',
        ),
        create=extend_schema(
            tags=[tag],
            summary=f'Crear {singular}',
            description=f'Registra {singular} nuevo.',
        ),
        update=extend_schema(
            tags=[tag],
            summary=f'Actualizar {singular}',
            description=f'Reemplaza todos los campos de {singular}.',
        ),
        partial_update=extend_schema(
            tags=[tag],
            summary=f'Actualizar parcialmente {singular}',
            description=f'Modifica solo los campos enviados de {singular}.',
        ),
        destroy=extend_schema(
            tags=[tag],
            summary=f'Eliminar {singular}',
            description=(
                f'Elimina {singular} de forma lógica (soft delete): '
                'el registro no se borra de la base de datos, solo se marca como eliminado.'
            ),
        ),
    )


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


@crud_schema(
    tag='Estados',
    singular='un estado',
    plural='estados',
    list_description=(
        'Devuelve la lista paginada de estados de México.\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre` o `clave`.'
    ),
)
class CatEstadoViewSet(SoftDeleteModelViewSet):
    """Catálogo de estados de México."""
    queryset = CatEstado.active_objects.all().order_by('id')
    serializer_class = CatEstadoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']


@crud_schema(
    tag='Municipios',
    singular='un municipio',
    plural='municipios',
    list_description=(
        'Devuelve la lista paginada de municipios.\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre` o `clave`.\n\n'
        '**Filtros:** `estado_id` devuelve solo los municipios de un estado.'
    ),
)
class CatMunicipioViewSet(SoftDeleteModelViewSet):
    """Catálogo de municipios de México."""
    queryset = CatMunicipio.active_objects.all().order_by('id')
    serializer_class = CatMunicipioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']
    filterset_fields = ['estado_id']


@crud_schema(
    tag='Ciudades',
    singular='una ciudad',
    plural='ciudades',
    list_description=(
        'Devuelve la lista paginada de ciudades.\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre`.\n\n'
        '**Filtros:** `estado_id` devuelve solo las ciudades de un estado.'
    ),
)
class CatCiudadViewSet(SoftDeleteModelViewSet):
    """Catálogo de ciudades de México."""
    queryset = CatCiudad.active_objects.all().order_by('id')
    serializer_class = CatCiudadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    filterset_fields = ['estado_id']


@crud_schema(
    tag='Tipos de asentamiento',
    singular='un tipo de asentamiento',
    plural='tipos de asentamiento',
    list_description=(
        'Devuelve la lista paginada de tipos de asentamiento '
        '(colonia, fraccionamiento, barrio, pueblo, etc.).\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre` o `clave`.'
    ),
)
class CatTipoAsentamientoViewSet(SoftDeleteModelViewSet):
    """Catálogo de tipos de asentamiento."""
    queryset = CatTipoAsentamiento.active_objects.all().order_by('id')
    serializer_class = CatTipoAsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'clave']


@crud_schema(
    tag='Zonas de asentamiento',
    singular='una zona de asentamiento',
    plural='zonas de asentamiento',
    list_description=(
        'Devuelve la lista paginada de zonas de asentamiento (urbana, rural, etc.).\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre`.'
    ),
)
class CatZonaAsentamientoViewSet(SoftDeleteModelViewSet):
    """Catálogo de zonas de asentamiento."""
    queryset = CatZonaAsentamiento.active_objects.all().order_by('id')
    serializer_class = CatZonaAsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


@crud_schema(
    tag='Códigos postales',
    singular='un código postal',
    plural='códigos postales',
    list_description=(
        'Devuelve la lista paginada de códigos postales.\n\n'
        '**Búsqueda:** use `search` para buscar por `codigo` (por ejemplo, `45010`).\n\n'
        '**Filtros:** `municipio_id` y `ciudad_id` limitan los resultados '
        'al municipio o ciudad indicados.'
    ),
)
class CodigoPostalViewSet(SoftDeleteModelViewSet):
    """Gestión de códigos postales."""
    queryset = CodigoPostal.active_objects.all().order_by('id')
    serializer_class = CodigoPostalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['codigo']
    filterset_fields = ['municipio_id', 'ciudad_id']


@extend_schema(
    tags=['Códigos postales'],
    summary='Detalle de un código postal',
    description=(
        'Devuelve la información completa de un código postal: municipio, ciudad '
        'y asentamientos asociados. Requiere autenticación (token JWT). '
        'Los registros eliminados lógicamente no se incluyen.'
    ),
    parameters=[
        OpenApiParameter(
            name='codigo',
            location=OpenApiParameter.PATH,
            description='Código postal de 5 dígitos (por ejemplo, `45010`).',
            type=str,
        ),
    ],
    responses={
        200: CodigoPostalDetailSerializer,
        404: None,
    },
)
class CodigoPostalDetailsView(RetrieveAPIView):
    serializer_class = CodigoPostalDetailSerializer

    def get_object(self):
        codigo = self.kwargs.get('codigo')

        return get_object_or_404(
            CodigoPostal.objects.filter(deleted_at__isnull=True),
            codigo=codigo
        )


@crud_schema(
    tag='Asentamientos',
    singular='un asentamiento',
    plural='asentamientos',
    list_description=(
        'Devuelve la lista paginada de asentamientos '
        '(colonias, fraccionamientos, barrios, etc.).\n\n'
        '**Búsqueda:** use `search` para filtrar por `nombre`.\n\n'
        '**Filtros:** `codigo_postal_id`, `tipo_asentamiento_id` y `zona_id` '
        'permiten acotar los resultados.'
    ),
)
class AsentamientoViewSet(SoftDeleteModelViewSet):
    """Gestión de asentamientos."""
    queryset = Asentamiento.active_objects.all().order_by('id')
    serializer_class = AsentamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    filterset_fields = ['codigo_postal_id', 'tipo_asentamiento_id', 'zona_id']