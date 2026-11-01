from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CatEstadoViewSet,
    CatMunicipioViewSet,
    CatCiudadViewSet,
    CatTipoAsentamientoViewSet,
    CatZonaAsentamientoViewSet,
    CodigoPostalViewSet,
    AsentamientoViewSet,
)

router = DefaultRouter()
router.register(r'estados', CatEstadoViewSet, basename='estado')
router.register(r'municipios', CatMunicipioViewSet, basename='municipio')
router.register(r'ciudades', CatCiudadViewSet, basename='ciudad')
router.register(r'tipos-asentamiento', CatTipoAsentamientoViewSet, basename='tipo-asentamiento')
router.register(r'zonas-asentamiento', CatZonaAsentamientoViewSet, basename='zona-asentamiento')
router.register(r'codigos-postales', CodigoPostalViewSet, basename='codigo-postal')
router.register(r'asentamientos', AsentamientoViewSet, basename='asentamiento')

urlpatterns = [
    path('', include(router.urls)),
]