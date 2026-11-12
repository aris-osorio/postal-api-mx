from rest_framework import serializers
from .models import (
    CatEstado,
    CatMunicipio,
    CatCiudad,
    CatTipoAsentamiento,
    CatZonaAsentamiento,
    CodigoPostal,
    Asentamiento,
)


class CatEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEstado
        fields = ['id', 'clave', 'nombre', 'created_at', 'updated_at']


class CatMunicipioSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.ReadOnlyField(source='estado_id.nombre')

    class Meta:
        model = CatMunicipio
        fields = ['id', 'clave', 'nombre', 'estado_id', 'estado_nombre', 'created_at', 'updated_at']


class CatCiudadSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.ReadOnlyField(source='estado_id.nombre')

    class Meta:
        model = CatCiudad
        fields = ['id', 'nombre', 'estado_id', 'estado_nombre', 'created_at', 'updated_at']


class CatTipoAsentamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTipoAsentamiento
        fields = ['id', 'clave', 'nombre', 'created_at', 'updated_at']


class CatZonaAsentamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatZonaAsentamiento
        fields = ['id', 'nombre', 'created_at', 'updated_at']


class CodigoPostalSerializer(serializers.ModelSerializer):
    municipio_nombre = serializers.ReadOnlyField(source='municipio_id.nombre')
    ciudad_nombre = serializers.ReadOnlyField(source='ciudad_id.nombre', default=None)

    class Meta:
        model = CodigoPostal
        fields = ['id', 'codigo', 'municipio_id', 'municipio_nombre', 'ciudad_id', 'ciudad_nombre', 'created_at', 'updated_at']


class AsentamientoSerializer(serializers.ModelSerializer):
    codigo_postal = serializers.ReadOnlyField(source='codigo_postal_id.codigo')
    tipo_asentamiento = serializers.ReadOnlyField(source='tipo_asentamiento_id.nombre')
    zona = serializers.ReadOnlyField(source='zona_id.nombre')

    class Meta:
        model = Asentamiento
        fields = [
            'id', 
            'nombre', 
            'codigo_postal_id', 
            'codigo_postal', 
            'tipo_asentamiento_id', 
            'tipo_asentamiento', 
            'zona_id', 
            'zona', 
            'created_at', 
            'updated_at'
        ]


class CodigoPostalDetailSerializer(serializers.ModelSerializer):
    municipio = serializers.CharField(source='municipio_id.nombre', read_only=True)
    estado = serializers.CharField(source='municipio_id.estado_id.nombre', read_only=True)
    ciudad = serializers.CharField(source='ciudad_id.nombre', allow_null=True, read_only=True)
    asentamientos = serializers.SerializerMethodField()

    class Meta:
        model = CodigoPostal
        fields = [
            'codigo',
            'municipio',
            'estado',
            'ciudad',
            'asentamientos'
        ]

    def get_asentamientos(self, obj):
        asentamientos_activos = Asentamiento.active_objects.filter(
            codigo_postal_id=obj, 
            deleted_at__isnull=True
        ).values_list('nombre', flat=True)
        
        return list(asentamientos_activos)