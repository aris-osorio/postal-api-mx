# Postal MX

API REST y panel de administración en Django para la consulta, validación y gestión de datos postales de México (Estados, Ciudades, Municipios, Códigos Postales y Asentamientos).

## Requisitos del Sistema

- **Python:** 3.10 o superior
- **Motor de Base de Datos:** PostgreSQL
- **Gestor de paquetes:** `pip` y entorno virtual (`venv` o `conda`)

## Guía de Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/postal-api-mx.git
cd postal-api-mx
```

### 2. Configurar el Entorno Virtual

**En Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows (PowerShell / CMD):**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generar SECRET_KEY de Django

Para generar una clave secreta única y segura para tu entorno local o de desarrollo, ejecuta el siguiente comando en la terminal:

```bash
python -c 'import django.core.management.utils; print(django.core.management.utils.get_random_secret_key())'
```

Copia la clave generada para pegarla en tu archivo `.env` en el paso siguiente.

### 5. Configurar Variables de Entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto para conectar la aplicación con tu base de datos PostgreSQL utilizando la siguiente plantilla:

```env
# BASE
DEBUG=True
SECRET_KEY='tu_secret_key_generada_aqui'
ALLOWED_HOSTS=*
API_BASE_URL=http://127.0.0.1:8000

# PostgreSQL
DB_NAME=nombre_de_tu_db
DB_USER=usuario_de_tu_db
DB_PASSWORD=contrasena_segura_db
DB_HOST=localhost
DB_PORT=5432
```

`API_BASE_URL` es la URL base que se muestra en la documentación interactiva. En producción cámbiala por tu dominio (por ejemplo, `https://tu-dominio.com`).

> **Nota de seguridad:** Nunca subas el archivo `.env` a tu repositorio remoto. Asegúrate de incluir `.env` dentro del archivo `.gitignore`.

### 6. Configuración de PostgreSQL

Antes de aplicar las migraciones, debes crear la base de datos, el usuario y asignar los permisos requeridos ejecutando las siguientes instrucciones desde la consola de PostgreSQL:

1. **Entrar a PostgreSQL vía consola:**
   ```bash
   psql -U postgres
   ```

2. **Crear la base de datos:**
   ```sql
   CREATE DATABASE nombre_de_tu_db;
   ```

3. **Crear usuario para esta base de datos:**
   ```sql
   CREATE USER usuario_de_tu_db WITH PASSWORD 'contrasena_segura_db';
   ```

4. **Asignarle privilegios al nuevo usuario sobre la nueva base de datos:**
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE nombre_de_tu_db TO usuario_de_tu_db;
   ```

5. **Asignar acceso al esquema público (requerido para PostgreSQL > v15):**
   ```sql
   \connect nombre_de_tu_db;
   GRANT CREATE ON SCHEMA public TO usuario_de_tu_db;
   ```

6. **Revisar la conexión del proyecto con PostgreSQL:**
   ```bash
   python manage.py check
   ```

   Debe retornar la confirmación exitosa:
   ```text
   System check identified no issues (0 silenced).
   ```

### 7. Aplicar Migraciones

Prepara la estructura de la base de datos en PostgreSQL:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Cargar Datos Postales Iniciales (Sepomex)

Ejecuta el comando o fixture correspondiente para poblar la base de datos con el catálogo postal:

```bash
python manage.py loaddata postal_data.json
# o bien:
# python manage.py import_sepomex
```

### 9. Recolectar Archivos Estáticos

Asegúrate de preparar los archivos estáticos para la interfaz de administración y la API:

```bash
python manage.py collectstatic --noinput
```

### 10. Crear Usuario Administrador

```bash
python manage.py createsuperuser
```

### 11. Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en `http://127.0.0.1:8000/`.

## Estructura del Proyecto

```text
postal-api-mx/
├── config/              # Configuración principal del proyecto (settings, urls, wsgi/asgi)
├── core/                # Funcionalidades base y utilidades generales
├── postal/              # Aplicación principal (Modelos, Vistas, Serializadores, Admin)
│   ├── migrations/      # Historial de migraciones de base de datos
│   ├── models.py        # Modelos (Estado, Municipio, Ciudad, Asentamiento, CP)
│   ├── serializers.py   # Serializadores de Django REST Framework
│   ├── views.py         # Endpoints y lógica de la API
│   └── urls.py          # Rutas locales de la app postal
├── static/              # Archivos estáticos en desarrollo
├── staticfiles/         # Archivos recolectados en producción (collectstatic)
├── .env                 # Variables de entorno (excluido de git)
├── .gitignore
├── manage.py
└── requirements.txt
```

## Endpoints de la API REST

### Autenticación

La API usa tokens JWT. Todos los endpoints requieren un token de acceso en el encabezado `Authorization`.

| Método HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| **POST** | `/api/v1/token/` | Recibe `username` y `password` y devuelve los tokens `access` y `refresh` (`AuthTokenObtainPairView`). |
| **POST** | `/api/v1/token/refresh/` | Recibe un `refresh` válido y devuelve un nuevo `access` (`AuthTokenRefreshView`). |

Ejemplo de petición para obtener los tokens:

```json
{
    "username": "mi_usuario",
    "password": "mi_contraseña"
}
```

Respuesta:

```json
{
    "refresh": "eyJhbGciOi...",
    "access": "eyJhbGciOi..."
}
```

Para consumir cualquier otro endpoint, envía el token de acceso en cada petición:

```text
Authorization: Bearer <access>
```

### Recursos

La API expone los siguientes recursos a través del enrutador por defecto (`DefaultRouter`) y vistas personalizadas:

| Método HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET / POST** | `/api/v1/estados/` | Lista o registra estados (`CatEstadoViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/estados/<id>/` | Detalle, edición y borrado de un estado. |
| **GET / POST** | `/api/v1/municipios/` | Lista o registra municipios (`CatMunicipioViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/municipios/<id>/` | Detalle, edición y borrado de un municipio. |
| **GET / POST** | `/api/v1/ciudades/` | Lista o registra ciudades (`CatCiudadViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/ciudades/<id>/` | Detalle, edición y borrado de una ciudad. |
| **GET / POST** | `/api/v1/tipos-asentamiento/` | Catálogo de tipos de asentamiento (`CatTipoAsentamientoViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/tipos-asentamiento/<id>/` | Detalle de tipo de asentamiento. |
| **GET / POST** | `/api/v1/zonas-asentamiento/` | Catálogo de zonas de asentamiento (`CatZonaAsentamientoViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/zonas-asentamiento/<id>/` | Detalle de zona de asentamiento. |
| **GET / POST** | `/api/v1/codigos-postales/` | Lista o registra códigos postales (`CodigoPostalViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/codigos-postales/<id>/` | Detalle, edición y borrado de un código postal. |
| **GET** | `/api/v1/codigos-postales/detalles/<codigo>/` | Vista detallada por código postal de 5 dígitos (`CodigoPostalDetailsView`). |
| **GET / POST** | `/api/v1/asentamientos/` | Lista o registra asentamientos (`AsentamientoViewSet`). |
| **GET / PUT / DELETE** | `/api/v1/asentamientos/<id>/` | Detalle, edición y borrado de un asentamiento. |

## Pruebas Unitarias

Para ejecutar el suite de pruebas del proyecto:

```bash
python manage.py test
```
