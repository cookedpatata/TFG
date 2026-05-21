# Instalación y ejecución del proyecto

Para ejecutar correctamente la aplicación es necesario disponer de:

- Python instalado.
- PostgreSQL instalado y configurado.
- Acceso a terminal o línea de comandos.
- El repositorio del proyecto descargado.

---

# 1. Descargar el proyecto

El primer paso consiste en descargar o clonar el repositorio del proyecto y acceder a la carpeta principal desde terminal.

```bash
git clone https://github.com/cookedpatata/TFG.git
cd nombre_del_proyecto
```

---

# 2. Crear el entorno virtual

Se recomienda crear un entorno virtual de Python para aislar las dependencias del proyecto y evitar conflictos con otras librerías instaladas en el sistema.

## Crear entorno virtual

```bash
python -m venv venv
```

## Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

---

# 3. Instalar dependencias

Con el entorno virtual activado, se deben instalar todas las dependencias necesarias del proyecto mediante el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

Este archivo contiene todas las librerías utilizadas durante el desarrollo de la aplicación.

---

# 4. Crear la base de datos

Antes de ejecutar el proyecto es necesario instalar PostgreSQL versión 17, utilizada durante el desarrollo de la aplicación.

Descarga oficial:

https://www.postgresql.org/download/

Una vez instalado PostgreSQL, debe crearse una base de datos destinada exclusivamente al proyecto.

La estructura completa de la base de datos se encuentra incluida dentro del archivo SQL proporcionado junto al proyecto (`BD.sql`).

Este archivo contiene:

- creación de tablas,
- relaciones,
- claves foráneas,
- restricciones,
- y estructura general del sistema.

Para generar toda la estructura de la base de datos, únicamente es necesario ejecutar el archivo SQL sobre PostgreSQL utilizando una herramienta compatible como:

- pgAdmin,
- consola `psql`,
- o cualquier cliente SQL compatible con PostgreSQL.

La base de datos almacenará toda la información relacionada con:

- usuarios,
- carreras,
- participantes,
- caballos,
- apuestas,
- resultados,
- y demás entidades del sistema.

---

# 5. Configurar settings.py

Después de crear la base de datos, es necesario modificar la configuración de conexión dentro del archivo `settings.py` de Django.

En el apartado `DATABASES` deben configurarse:

- nombre de la base de datos,
- usuario,
- contraseña,
- host,
- y puerto.

Ejemplo de configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'TFG',
        'USER': 'postgres',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Además, dependiendo del entorno donde se ejecute la aplicación, también puede ser necesario modificar:

- `ALLOWED_HOSTS`,
- `DEBUG`,
- configuración de archivos estáticos,
- y rutas de plantillas.

---

# 6. Ejecutar migraciones

Una vez configurada la base de datos, deben ejecutarse las migraciones de Django.

## Crear migraciones

```bash
python manage.py makemigrations
```

## Aplicar migraciones

```bash
python manage.py migrate
```

El sistema de migraciones se encarga de crear automáticamente todas las tablas necesarias dentro de PostgreSQL a partir de los modelos definidos en la aplicación.

---

# 7. Crear superusuario

Tras completar las migraciones, debe crearse un superusuario de Django.

```bash
python manage.py createsuperuser
```

Durante la creación del superusuario se solicitarán:

- nombre de usuario,
- correo electrónico,
- y contraseña.

---

# 8. Ejecutar la aplicación

Finalmente, la aplicación puede iniciarse utilizando el servidor de desarrollo integrado de Django.

---

# 9. Acceder al panel de administración

Una vez iniciado el proyecto, el panel administrativo estará disponible mediante la ruta:

```text
/admin
```

Desde esta interfaz es posible:

- gestionar usuarios,
- administrar carreras,
- modificar participantes,
- consultar apuestas,
- y controlar gran parte de la información almacenada en el sistema.

La interfaz administrativa de Django incorpora automáticamente:

- autenticación,
- gestión de permisos,
- sesiones,
- y administración de modelos.

```bash
python manage.py runserver
```

Una vez iniciado el servidor, la aplicación estará disponible desde navegador web y lista para su utilización.
