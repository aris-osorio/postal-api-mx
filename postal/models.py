from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class CatEstado(BaseModel):
    clave = models.CharField(max_length=2, unique=True, help_text="Clave oficial (ej. '01', '09', '14')")
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'cat_estados'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return f"{self.clave} - {self.nombre}"


class CatMunicipio(BaseModel):
    estado_id = models.ForeignKey(CatEstado, on_delete=models.PROTECT, db_column='estado_id')
    clave = models.CharField(max_length=3, help_text="Clave de municipio por estado")
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'cat_municipios'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        constraints = [
            models.UniqueConstraint(fields=['estado_id', 'clave'], name='uk_municipio_estado')
        ]

    def __str__(self):
        return f"{self.nombre} ({self.estado_id.nombre})"


class CatCiudad(BaseModel):
    estado_id = models.ForeignKey(CatEstado, on_delete=models.PROTECT, db_column='estado_id')
    clave = models.CharField(max_length=3, help_text="Clave de ciudad por estado", default="")
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'cat_ciudades'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre


class CodigoPostal(BaseModel):
    codigo = models.CharField(
        max_length=5, 
        unique=True, 
        help_text="Código Postal a 5 dígitos (preserva ceros iniciales como '01000')"
    )
    municipio_id = models.ForeignKey(CatMunicipio, on_delete=models.PROTECT, db_column='municipio_id')
    ciudad_id = models.ForeignKey(
        CatCiudad, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='ciudad_id'
    )

    class Meta:
        db_table = 'codigos_postales'
        verbose_name = 'Código Postal'
        verbose_name_plural = 'Códigos Postales'

    def __str__(self):
        return self.codigo


class CatTipoAsentamiento(BaseModel):
    clave = models.CharField(max_length=2, unique=True, help_text="Clave de asentamiento")
    nombre = models.CharField(max_length=100, unique=True, help_text="Ej: Colonia, Ejido, Fraccionamiento")

    class Meta:
        db_table = 'cat_tipos_asentamiento'
        verbose_name = 'Tipo de Asentamiento'
        verbose_name_plural = 'Tipos de Asentamiento'

    def __str__(self):
        return self.nombre


class CatZonaAsentamiento(BaseModel):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Urbano, Rural")

    class Meta:
        db_table = 'cat_zonas_asentamientos'
        verbose_name = 'Zona de Asentamiento'
        verbose_name_plural = 'Zonas de Asentamiento'

    def __str__(self):
        return self.nombre


class Asentamiento(BaseModel):
    codigo_postal_id = models.ForeignKey(
        CodigoPostal, 
        on_delete=models.PROTECT, 
        db_column='codigo_postal_id'
    )
    tipo_asentamiento_id = models.ForeignKey(
        CatTipoAsentamiento, 
        on_delete=models.PROTECT, 
        db_column='tipo_asentamiento_id'
    )
    zona_id = models.ForeignKey(
        CatZonaAsentamiento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='zona_id'
    )
    nombre = models.CharField(max_length=150, help_text="Nombre de la colonia o localidad")

    class Meta:
        db_table = 'asentamientos'
        verbose_name = 'Asentamiento'
        verbose_name_plural = 'Asentamientos'
        indexes = [
            models.Index(fields=['nombre', 'codigo_postal_id'], name='idx_asentamiento_busqueda'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_postal_id.codigo})"
