from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    CatEstado,
    CatMunicipio,
    CatCiudad,
    CatTipoAsentamiento,
    CatZonaAsentamiento,
    CodigoPostal,
    Asentamiento,
)


@admin.register(CatEstado)
class CatEstadoAdmin(ModelAdmin):
    list_display = ('clave', 'nombre', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CatEstado.all_objects.all()


@admin.register(CatMunicipio)
class CatMunicipioAdmin(ModelAdmin):
    list_display = ('clave', 'nombre', 'estado_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre', 'estado_id__nombre')
    list_filter = ('estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CatMunicipio.all_objects.all()


@admin.register(CatCiudad)
class CatCiudadAdmin(ModelAdmin):
    list_display = ('nombre', 'estado_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('nombre', 'estado_id__nombre')
    list_filter = ('estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CatCiudad.all_objects.all()


@admin.register(CatTipoAsentamiento)
class CatTipoAsentamientoAdmin(ModelAdmin):
    list_display = ('clave', 'nombre', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CatTipoAsentamiento.all_objects.all()


@admin.register(CatZonaAsentamiento)
class CatZonaAsentamientoAdmin(ModelAdmin):
    list_display = ('nombre', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('nombre',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CatZonaAsentamiento.all_objects.all()


@admin.register(CodigoPostal)
class CodigoPostalAdmin(ModelAdmin):
    list_display = ('codigo', 'municipio_id', 'ciudad_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('codigo', 'municipio_id__nombre')
    list_filter = ('municipio_id__estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return CodigoPostal.all_objects.all()


@admin.register(Asentamiento)
class AsentamientoAdmin(ModelAdmin):
    list_display = ('nombre', 'codigo_postal_id', 'tipo_asentamiento_id', 'zona_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('nombre', 'codigo_postal_id__codigo')
    list_filter = ('tipo_asentamiento_id', 'zona_id')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        return Asentamiento.all_objects.all()
