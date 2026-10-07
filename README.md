# Gestión de Contactos — Django

Aplicación web de gestión de contactos desarrollada con **Python y Django**. El proyecto permite registrar usuarios, iniciar sesión y gestionar contactos asociados a cada usuario y a una provincia.

La aplicación se ha desarrollado como una segunda implementación de un proyecto de gestión de contactos realizado originalmente con Symfony/PHP, con el objetivo de aplicar los mismos conceptos utilizando Django.

---

## 📋 Características

- Registro de usuarios.
- Inicio y cierre de sesión.
- Gestión de contactos mediante CRUD completo.
- Creación de contactos.
- Consulta del detalle de un contacto.
- Edición de contactos.
- Eliminación de contactos con confirmación.
- Asociación de cada contacto a un usuario.
- Asociación de cada contacto a una provincia.
- Cada usuario puede consultar y gestionar únicamente sus propios contactos.
- Formularios realizados con Django Forms.
- Autenticación mediante el sistema integrado de Django.
- Diseño personalizado mediante CSS.
- Diseño responsive para diferentes tamaños de pantalla.
- Base de datos SQLite.
- Uso del ORM de Django.
- Sistema de archivos estáticos de Django.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| **Python 3.12.3** | Lenguaje de programación |
| **Django 6.1.1** | Framework web |
| **SQLite** | Base de datos |
| **Django ORM** | Acceso y gestión de datos |
| **Django Templates** | Generación de páginas HTML |
| **Django Forms** | Formularios y validación |
| **Django Auth** | Registro y autenticación |
| **HTML5** | Estructura de las páginas |
| **CSS3** | Diseño e interfaz |

---

## 📁 Estructura del proyecto

```text
djengo-contactos/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── contactos/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   │
│   ├── static/
│   │   └── contactos/
│   │       └── estilos.css
│   │
│   ├── templates/
│   │   └── contactos/
│   │       ├── inicio.html
│   │       ├── anadir_contacto.html
│   │       ├── detalle_contacto.html
│   │       ├── editar_contacto.html
│   │       ├── eliminar_contacto.html
│   │       ├── login.html
│   │       └── registro.html
│   │
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── db.sqlite3
├── manage.py
└── venv/
```

---

## 🗄️ Modelos

La aplicación utiliza dos modelos principales: `Provincia` y `Contacto`.

### Provincia

Representa las provincias disponibles para asociarlas a los contactos.

```python
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
```

### Contacto

Representa un contacto y contiene información personal y sus relaciones con una provincia y un usuario.

```python
class Contacto(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre
```

### Relaciones

```text
User
 │
 └── Contacto
       │
       └── Provincia
```

Cada contacto pertenece a un usuario y está asociado a una provincia.

---

## 🔐 Sistema de usuarios

La aplicación utiliza el sistema de autenticación integrado de Django.

### Registro

Se utiliza `UserCreationForm` para crear nuevos usuarios:

```python
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
```

El registro permite introducir:

- Nombre de usuario.
- Email.
- Contraseña.
- Confirmación de contraseña.

Django se encarga de las validaciones y del almacenamiento seguro de las contraseñas.

### Login

Se utiliza `LoginView` de Django para gestionar el inicio de sesión.

### Logout

El cierre de sesión se realiza mediante una petición `POST` con protección CSRF.

```html
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}

    <button type="submit">
        Cerrar sesión
    </button>
</form>
```

---

## 👤 Protección de los contactos

Los contactos están asociados al usuario que los ha creado.

Para obtener únicamente los contactos del usuario autenticado se utiliza:

```python
Contacto.objects.filter(usuario=request.user)
```

Para acceder a un contacto concreto también se comprueba el propietario:

```python
get_object_or_404(
    Contacto,
    id=id,
    usuario=request.user
)
```

Esto evita que un usuario pueda consultar, modificar o eliminar los contactos pertenecientes a otro usuario.

Las vistas que requieren autenticación utilizan:

```python
@login_required
```

---

## 📇 CRUD de contactos

La aplicación implementa las cuatro operaciones principales del CRUD:

### Crear

Ruta:

```text
/contacto/nuevo/
```

Se utiliza `ContactoForm`:

```python
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = [
            'nombre',
            'telefono',
            'email',
            'provincia'
        ]
```

El usuario propietario se asigna automáticamente:

```python
contacto = formulario.save(commit=False)
contacto.usuario = request.user
contacto.save()
```

### Leer

Ruta:

```text
/contacto/<id>/
```

Permite consultar los datos completos de un contacto.

### Actualizar

Ruta:

```text
/contacto/<id>/editar/
```

Se reutiliza `ContactoForm` pasando la instancia existente:

```python
formulario = ContactoForm(
    request.POST,
    instance=contacto
)
```

### Eliminar

Ruta:

```text
/contacto/<id>/eliminar/
```

Antes de eliminar el contacto se muestra una página de confirmación.

La eliminación definitiva se realiza mediante `POST`:

```python
contacto.delete()
```

---

## 🌐 Rutas principales

| Ruta | Función |
|---|---|
| `/` | Página principal |
| `/login/` | Inicio de sesión |
| `/logout/` | Cierre de sesión |
| `/registro/` | Registro de usuarios |
| `/contacto/nuevo/` | Crear contacto |
| `/contacto/<id>/` | Ver contacto |
| `/contacto/<id>/editar/` | Editar contacto |
| `/contacto/<id>/eliminar/` | Eliminar contacto |

---

## 🎨 Diseño y CSS

El diseño se ha realizado mediante un archivo CSS propio:

```text
contactos/static/contactos/estilos.css
```

Las plantillas cargan el archivo mediante el sistema de archivos estáticos de Django:

```django
{% load static %}

<link rel="stylesheet" href="{% static 'contactos/estilos.css' %}">
```

### Elementos del diseño

- Fondo degradado.
- Tarjetas para los contactos.
- Botones diferenciados por función.
- Formularios estilizados.
- Tarjetas de detalle.
- Sombras y bordes redondeados.
- Efectos `hover`.
- Diseño responsive.

Entre las clases principales se encuentran:

```text
.container
.header
.contact-card
.contact-info
.contact-actions
.form-container
.detail-card
.detail-item
.empty
.btn
.btn-primary
.btn-edit
.btn-danger
.btn-secondary
```

---

## 🧩 Plantillas

La aplicación dispone de las siguientes plantillas:

| Plantilla | Función |
|---|---|
| `inicio.html` | Lista de contactos |
| `anadir_contacto.html` | Formulario de creación |
| `detalle_contacto.html` | Información del contacto |
| `editar_contacto.html` | Formulario de edición |
| `eliminar_contacto.html` | Confirmación de eliminación |
| `login.html` | Inicio de sesión |
| `registro.html` | Registro de usuarios |

Todas utilizan el mismo archivo CSS para mantener una apariencia coherente.

---

## 🗃️ Base de datos

Se utiliza **SQLite** como sistema de base de datos.

El archivo se encuentra en:

```text
db.sqlite3
```

Además de las tablas propias de la aplicación, Django genera tablas para funcionalidades internas como:

- Usuarios.
- Grupos.
- Permisos.
- Sesiones.
- Administración.

La base de datos también puede abrirse y consultarse mediante herramientas como **DBeaver**.

---

## 🔄 Migraciones

Django utiliza su sistema de migraciones para gestionar los cambios realizados en los modelos.

Crear migraciones:

```bash
python manage.py makemigrations
```

Aplicarlas:

```bash
python manage.py migrate
```

Durante el desarrollo se produjo un problema al añadir el campo `usuario` como obligatorio a un modelo que ya tenía una migración anterior. También existían migraciones en un orden incorrecto.

Al encontrarse el proyecto todavía en fase inicial y no ser necesario conservar los datos de prueba, se regeneraron las migraciones de la aplicación y se creó una nueva migración inicial.

Actualmente:

```text
contactos/migrations/
├── 0001_initial.py
└── __init__.py
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd djengo-contactos
```

### 2. Crear el entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

En Linux:

```bash
source venv/bin/activate
```

### 4. Instalar Django

```bash
pip install django
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Crear un superusuario si fuese necesario

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

---

## 🔧 Comandos principales

| Comando | Función |
|---|---|
| `source venv/bin/activate` | Activar el entorno virtual |
| `python manage.py runserver` | Iniciar el servidor |
| `python manage.py makemigrations` | Crear migraciones |
| `python manage.py migrate` | Aplicar migraciones |
| `python manage.py startapp contactos` | Crear una aplicación |
| `python manage.py createsuperuser` | Crear superusuario |
| `python manage.py findstatic contactos/estilos.css` | Comprobar un archivo estático |

---

## 🐛 Problemas resueltos durante el desarrollo

### Campo `usuario` no nullable

Al añadir el campo `usuario` a `Contacto`, Django solicitó un valor por defecto para los registros existentes.

Se solucionó regenerando las migraciones y la base de datos durante la fase inicial del proyecto.

### Nombre de función `anadir_contacto`

Se produjo un conflicto entre el nombre de la vista y el nombre utilizado en las URLs debido al uso de la letra `ñ`.

Se estableció el nombre:

```python
anadir_contacto
```

para evitar problemas con identificadores Python.

### Archivos estáticos

El archivo CSS se encontraba en:

```text
contactos/static/contactos/estilos.css
```

La referencia correcta desde las plantillas es:

```django
{% static 'contactos/estilos.css' %}
```

La localización del archivo puede comprobarse con:

```bash
python manage.py findstatic contactos/estilos.css
```

### Error 405 al cerrar sesión

Inicialmente se utilizó un enlace GET para cerrar sesión. Django devolvía:

```text
405 Method Not Allowed
```

Se solucionó utilizando un formulario `POST` con `{% csrf_token %}`.

---

## 🔄 Equivalencias Symfony ↔ Django

El proyecto se ha desarrollado como una segunda implementación de conceptos trabajados anteriormente con Symfony.

| Symfony | Django |
|---|---|
| PHP | Python |
| Symfony | Django |
| Controller | View |
| Entity | Model |
| Doctrine ORM | Django ORM |
| Twig | Django Templates |
| Doctrine Migrations | Django Migrations |
| Composer | pip |
| Symfony Security | Django Authentication |

La arquitectura general puede resumirse como:

```text
Django

View
 ↓
Model
 ↓
Django ORM
 ↓
SQLite
 ↓
Template
```

---

## 📌 Estado actual

El proyecto cuenta actualmente con una base funcional de gestión de contactos:

- [x] Configuración del proyecto Django.
- [x] Entorno virtual.
- [x] Base de datos SQLite.
- [x] Modelo `Provincia`.
- [x] Modelo `Contacto`.
- [x] Relación Contacto → Provincia.
- [x] Relación Contacto → Usuario.
- [x] Migraciones.
- [x] Listado de contactos.
- [x] Crear contactos.
- [x] Ver contactos.
- [x] Editar contactos.
- [x] Eliminar contactos.
- [x] Registro de usuarios.
- [x] Login.
- [x] Logout.
- [x] Protección mediante autenticación.
- [x] Separación de contactos por usuario.
- [x] Formularios Django.
- [x] CSS personalizado.
- [x] Diseño responsive.

---

## 🔮 Posibles mejoras futuras

Algunas mejoras que pueden incorporarse posteriormente:

- Barra de navegación común.
- Sistema de mensajes de Django para confirmar operaciones.
- Validaciones adicionales para teléfono y email.
- Paginación de contactos.
- Búsqueda y filtrado.
- Mejoras adicionales en responsive design.
- Perfil de usuario.
- Cambio de contraseña.
- Recuperación de contraseña.
- Confirmaciones y mensajes de éxito/error más avanzados.
- Despliegue de la aplicación en un servidor.

---

## 📄 Licencia

Proyecto desarrollado con fines educativos.
