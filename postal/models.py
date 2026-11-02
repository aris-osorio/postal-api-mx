from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class CatEstado(BaseModel):
    clave = models.CharField(max_length=2, help_text="Clave oficial (ej. '01', '09', '14')")
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'cat_estados'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        constraints = [
            models.UniqueConstraint(
                fields=['clave'],
                condition=Q(deleted_at__isnull=True),
                name='unique_cat_estado_clave_activo'
            ),
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_cat_estado_nombre_activo'
            )
        ]
    
    def clean(self):
        super().clean()
        qs = CatEstado.objects.filter(Q(clave=self.clave) | Q(nombre__iexact=self.nombre))
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Ya existe un estado activo con esa clave o nombre.")

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
            models.UniqueConstraint(
                fields=['estado_id', 'clave'],
                condition=Q(deleted_at__isnull=True),
                name='unique_municipio_estado_clave_activo'
            ),
            models.UniqueConstraint(
                fields=['estado_id', 'nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_municipio_estado_nombre_activo'
            )
        ]
    
    def clean(self):
        super().clean()
        if self.estado_id_id:
            qs = CatMunicipio.objects.filter(
                estado_id=self.estado_id
            ).filter(Q(clave=self.clave) | Q(nombre__iexact=self.nombre))
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Ya existe un municipio activo con esa clave o nombre en este estado.")

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
        constraints = [
            models.UniqueConstraint(
                fields=['estado_id', 'clave'],
                condition=Q(deleted_at__isnull=True),
                name='unique_ciudad_estado_clave_activo'
            ),
            models.UniqueConstraint(
                fields=['estado_id', 'nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_ciudad_estado_nombre_activo'
            )
        ]
    
    def clean(self):
        super().clean()
        if self.estado_id_id:
            qs = CatCiudad.objects.filter(
                estado_id=self.estado_id
            ).filter(Q(clave=self.clave) | Q(nombre__iexact=self.nombre))
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Ya existe una ciudad activa con esa clave o nombre en este estado.")

    def __str__(self):
        return self.nombre


class CodigoPostal(BaseModel):
    codigo = models.CharField(
        max_length=5, 
        validators=[MinLengthValidator(5, message="El código postal debe tener exactamente 5 dígitos.")],
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
        constraints = [
            models.UniqueConstraint(
                fields=['codigo'],
                condition=Q(deleted_at__isnull=True),
                name='unique_codigo_postal_activo'
            )
        ]
    
    def clean(self):
        super().clean()
        qs = CodigoPostal.objects.filter(codigo=self.codigo)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Ya existe un código postal activo con ese código.")

    def __str__(self):
        return self.codigo


class CatTipoAsentamiento(BaseModel):
    clave = models.CharField(max_length=2, help_text="Clave de asentamiento")
    nombre = models.CharField(max_length=100, help_text="Ej: Colonia, Ejido, Fraccionamiento")

    class Meta:
        db_table = 'cat_tipos_asentamiento'
        verbose_name = 'Tipo de Asentamiento'
        verbose_name_plural = 'Tipos de Asentamiento'
        constraints = [
            models.UniqueConstraint(
                fields=['clave'],
                condition=Q(deleted_at__isnull=True),
                name='unique_tipo_asentamiento_clave_activo'
            ),
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_tipo_asentamiento_nombre_activo'
            )
        ]
    
    def clean(self):
        super().clean()
        qs = CatTipoAsentamiento.objects.filter(Q(clave=self.clave) | Q(nombre__iexact=self.nombre))
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Ya existe un tipo de asentamiento activo con esa clave o nombre.")

    def __str__(self):
        return self.nombre


class CatZonaAsentamiento(BaseModel):
    nombre = models.CharField(max_length=50, help_text="Ej: Urbano, Rural")

    class Meta:
        db_table = 'cat_zonas_asentamientos'
        verbose_name = 'Zona de Asentamiento'
        verbose_name_plural = 'Zonas de Asentamiento'
        constraints = [
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_zona_asentamiento_nombre_activo'
            )
        ]
        
    def clean(self):
        super().clean()
        qs = CatZonaAsentamiento.objects.filter(nombre__iexact=self.nombre)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Ya existe una zona de asentamiento activa con ese nombre.")

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
    nombre = models.CharField(max_length=150, help_text="Nombre del asentamiento")

    class Meta:
        db_table = 'asentamientos'
        verbose_name = 'Asentamiento'
        verbose_name_plural = 'Asentamientos'
        indexes = [
            models.Index(fields=['nombre', 'codigo_postal_id'], name='idx_asentamiento_busqueda'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['codigo_postal_id', 'nombre'],
                condition=Q(deleted_at__isnull=True),
                name='unique_asentamiento_cp_nombre_activo'
            )
        ]

    def clean(self):
        super().clean()
        if self.codigo_postal_id_id:
            qs = Asentamiento.objects.filter(
                codigo_postal_id=self.codigo_postal_id,
                nombre__iexact=self.nombre
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Ya existe un asentamiento activo con este nombre para el código postal seleccionado.")

    def __str__(self):
        return f"{self.nombre} ({self.codigo_postal_id.codigo})"
