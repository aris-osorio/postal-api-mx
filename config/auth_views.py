from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema(
    tags=['Autenticación'],
    summary='Iniciar sesión (obtener tokens)',
    description=(
        'Recibe `username` y `password` y devuelve un par de tokens JWT:\n\n'
        '- `access`: se envía en cada petición en el encabezado '
        '`Authorization: Bearer <access>`. Tiene una vida corta.\n'
        '- `refresh`: sirve para obtener un nuevo `access` sin volver a iniciar sesión.\n\n'
        'Si las credenciales son incorrectas responde `401`.'
    ),
    examples=[
        OpenApiExample(
            'Credenciales',
            value={'username': 'mi_usuario', 'password': 'mi_contraseña'},
            request_only=True,
        ),
        OpenApiExample(
            'Respuesta exitosa',
            value={'refresh': 'eyJhbGciOi...', 'access': 'eyJhbGciOi...'},
            response_only=True,
        ),
    ],
)
class AuthTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=['Autenticación'],
    summary='Renovar token de acceso',
    description=(
        'Recibe un token `refresh` válido y devuelve un nuevo token `access`.\n\n'
        'Si el `refresh` expiró o es inválido responde `401` y hay que '
        'iniciar sesión de nuevo.'
    ),
    examples=[
        OpenApiExample(
            'Petición',
            value={'refresh': 'eyJhbGciOi...'},
            request_only=True,
        ),
        OpenApiExample(
            'Respuesta exitosa',
            value={'access': 'eyJhbGciOi...'},
            response_only=True,
        ),
    ],
)
class AuthTokenRefreshView(TokenRefreshView):
    pass