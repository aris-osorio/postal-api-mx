from django.contrib import admin
from unfold.admin import ModelAdmin
from core.admin import ActiveObjectsAutocompleteMixin
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
class CatEstadoAdmin(ActiveObjectsAutocompleteMixin, ModelAdmin):
    list_display = ('clave', 'nombre', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


@admin.register(CatMunicipio)
class CatMunicipioAdmin(ActiveObjectsAutocompleteMixin, ModelAdmin):
    list_display = ('clave', 'nombre', 'estado_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre', 'estado_id__nombre')
    list_filter = ('estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    autocomplete_fields = ["estado_id"]
    list_select_related = ["estado_id"]
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


@admin.register(CatCiudad)
class CatCiudadAdmin(ModelAdmin):
    list_display = ('clave', 'nombre', 'estado_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('clave', 'nombre', 'estado_id__nombre')
    list_filter = ('estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    autocomplete_fields = ["estado_id"]
    list_select_related = ["estado_id"]
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


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
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


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
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


@admin.register(CodigoPostal)
class CodigoPostalAdmin(ModelAdmin):
    list_display = ('codigo', 'municipio_id', 'ciudad_id', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('codigo', 'municipio_id__nombre')
    list_filter = ('municipio_id__estado_id',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    autocomplete_fields = ["municipio_id", "ciudad_id"]
    list_select_related = ["municipio_id", "ciudad_id"]
    
    list_filter_submit = True
    list_show_full_result_count = False
    show_full_result_count = False 
    compressed_fields = True
    list_fullwidth = True

    def get_queryset(self, request):
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()


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
        manager = self.model.all_objects if request.user.is_superuser else self.model.active_objects
        return manager.all()
