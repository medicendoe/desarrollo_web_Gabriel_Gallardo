# 🏠 Portal de Adopción de Mascotas - Tarea 2 (CC5002)

Una aplicación web desarrollada en **Flask** con arquitectura modular completamente configurable para gestionar avisos de adopción de mascotas. Implementa todas las funcionalidades requeridas para la Tarea 2 con validación robusta, manejo de archivos y configuración portable.

## 🚀 Características Principales

### ✅ Funcionalidades Implementadas (Tarea 2)
- **🏠 Portada**: Muestra los últimos 5 avisos de adopción ordenados por fecha
- **📝 Formulario de Avisos**: Validación server-side completa con subida de fotos
- **📋 Listado Paginado**: 5 avisos por página con navegación entre páginas
- **🗺️ Ubicaciones**: Base de datos completa con regiones y comunas de Chile
- **📊 Estadísticas**: Panel con gráficos de adopciones por tipo y región

### �️ Características Técnicas
- **🔧 Configuración Portable**: Sin variables hardcodeadas, adaptable a cualquier entorno
- **🏗️ Arquitectura Modular**: Factory Pattern, Blueprints, separación de responsabilidades
- **�️ Validación Robusta**: Server-side validation con mensajes informativos
- **📸 Manejo de Archivos**: Subida múltiple de fotos con seguridad
- **💾 Base de Datos**: Relaciones correctas, transacciones seguras, rollback automático

## 🛠️ Tecnologías y Stack

- **Backend**: Python 3.13, Flask 3.0.0, SQLAlchemy ORM
- **Base de Datos**: MySQL/MariaDB con PyMySQL driver
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Configuración**: Variables de entorno con python-dotenv
- **Arquitectura**: Factory Pattern, Blueprints, Modular Design

## 📁 Estructura del Proyecto

```
daw/
├── 🏗️ app/                      # Aplicación Flask modular
│   ├── __init__.py              # Factory Pattern - create_app()
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── __init__.py          # Exportación de modelos
│   │   ├── region_comuna.py     # Region, Comuna (ubicaciones)
│   │   └── aviso.py             # AvisoAdopcion, Foto, ContactarPor
│   ├── routes/                  # Rutas organizadas en Blueprints
│   │   ├── __init__.py
│   │   ├── main.py              # Rutas principales web
│   │   └── api.py               # API REST endpoints
│   └── utils.py                 # Funciones utilitarias
├── 🔧 config/                   # Configuración completamente parametrizable
│   └── config.py                # Config por entorno (dev/prod/test)
├── 🎨 templates/                # Templates Jinja2
│   ├── index.html               # Portada con últimos 5 avisos
│   ├── agregar_aviso.html       # Formulario con validación
│   ├── listado_avisos.html      # Listado paginado
│   └── estadisticas.html        # Dashboard de estadísticas
├── 📦 static/                   # Archivos estáticos
│   ├── css/style.css            # Estilos responsive
│   ├── js/                      # JavaScript interactivo
│   └── uploads/                 # 📸 Fotos subidas (creado automáticamente)
├── 💾 data/                     # Scripts SQL y datos iniciales
│   ├── tarea2.sql               # Estructura de base de datos
│   └── region-comuna.sql        # Datos de regiones y comunas
├── 📋 Archivos de configuración
│   ├── .env.example             # Plantilla de variables de entorno
│   ├── CONFIG_GUIDE.md          # Guía detallada de configuración
│   ├── requirements.txt         # Dependencias Python
│   └── app.py                   # Punto de entrada principal
└── 🧪 test_insert.py           # Script de pruebas con datos ejemplo
```

## ⚡ Instalación y Configuración

### 1. 📋 Requisitos Previos
- **Python 3.13+** (recomendado con pyenv)
- **MySQL/MariaDB** (local, Docker, o servicio cloud)
- **Git** para clonar el repositorio

### 2. 🚀 Instalación Rápida

```bash
# 📥 Clonar el repositorio
git clone https://github.com/medicendoe/desarrollo_web_Gabriel_Gallardo.git
cd desarrollo_web_Gabriel_Gallardo

# 🐍 Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o .venv\Scripts\activate  # Windows

# 📦 Instalar dependencias
pip install -r requirements.txt
```

### 3. 🔧 Configuración de Variables de Entorno

#### **Paso 1: Crear archivo de configuración**
```bash
# Copiar plantilla de configuración
cp .env.example .env
```

#### **Paso 2: Configurar según tu entorno**

##### **🏠 Desarrollo Local (MySQL estándar)**
```bash
# Editar .env con:
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion

# Configuración de base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=cc5002
DB_PASSWORD=programacionweb
DB_NAME=tarea2

# Configuración de archivos
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

##### **🐳 Docker/Devbox (Socket Unix)**
```bash
# Añadir a .env:
USE_UNIX_SOCKET=true
MYSQL_UNIX_SOCKET=/tmp/mysql.sock
# (o la ruta específica de tu socket)
```

##### **☁️ Producción (URL completa)**
```bash
# Opción 1: URL completa
DATABASE_URL=mysql+pymysql://usuario:password@servidor.com:3306/tarea2

# Opción 2: Componentes individuales
DB_HOST=tu-servidor-produccion.com
DB_PORT=3306
DB_USER=usuario_prod
DB_PASSWORD=password_super_segura
DB_NAME=tarea2_prod
SECRET_KEY=clave-produccion-ultra-segura
```

### 4. 🗄️ Configuración de Base de Datos

#### **Opción A: MySQL Local**
```bash
# Crear base de datos y usuario
mysql -u root -p << EOF
CREATE DATABASE tarea2;
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
EOF

# Importar estructura y datos
mysql -u cc5002 -p tarea2 < data/tarea2.sql
mysql -u cc5002 -p tarea2 < data/region-comuna.sql
```

#### **Opción B: Docker MySQL**
```bash
# Ejecutar MySQL en Docker
docker run --name mysql-tarea2 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=tarea2 -e MYSQL_USER=cc5002 -e MYSQL_PASSWORD=programacionweb -p 3306:3306 -d mysql:8.0

# Importar datos (esperar que el contenedor esté listo)
sleep 10
docker exec -i mysql-tarea2 mysql -u cc5002 -pprogramacionweb tarea2 < data/tarea2.sql
docker exec -i mysql-tarea2 mysql -u cc5002 -pprogramacionweb tarea2 < data/region-comuna.sql
```

#### **Opción C: Devbox (Entorno reproducible)**
```bash
# Si tienes devbox instalado
devbox shell
devbox services up

# Configurar socket en .env
USE_UNIX_SOCKET=true
MYSQL_UNIX_SOCKET=/ruta/al/socket/mysql.sock

# Importar datos
devbox run mysql -u root tarea2 < data/tarea2.sql
devbox run mysql -u root tarea2 < data/region-comuna.sql
```

### 5. ▶️ Ejecutar Aplicación

```bash
# 🚀 Iniciar aplicación
python app.py

# 🌐 Acceder en el navegador
# http://127.0.0.1:5001
```

### 6. 🧪 Verificar Instalación (Opcional)

```bash
# Insertar datos de prueba
python test_insert.py

# Verificar que la BD esté funcionando
# Deberías ver: "✅ Aviso de prueba creado exitosamente"
```

## 🔧 Variables de Entorno Completas

### 📋 **Variables Principales (Obligatorias)**

| Variable | Descripción | Ejemplo | Por Defecto |
|----------|-------------|---------|-------------|
| `FLASK_ENV` | Entorno de ejecución | `development`, `production`, `testing` | `development` |
| `SECRET_KEY` | Clave secreta de Flask | `mi-clave-super-secreta-123` | ⚠️ **Cambiar en producción** |
| `DB_HOST` | Servidor de base de datos | `localhost`, `db.empresa.com` | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306`, `3307` | `3306` |
| `DB_USER` | Usuario de base de datos | `cc5002`, `usuario_app` | `cc5002` |
| `DB_PASSWORD` | Contraseña de BD | `programacionweb` | `programacionweb` |
| `DB_NAME` | Nombre de la base de datos | `tarea2`, `adopciones_prod` | `tarea2` |

### 🔧 **Variables Opcionales (Configuración Avanzada)**

| Variable | Descripción | Ejemplo | Por Defecto |
|----------|-------------|---------|-------------|
| `DATABASE_URL` | URL completa de BD (sobreescribe otros parámetros) | `mysql+pymysql://user:pass@host:port/db` | `None` |
| `USE_UNIX_SOCKET` | Usar socket Unix en lugar de TCP | `true`, `false` | `false` |
| `MYSQL_UNIX_SOCKET` | Ruta al socket MySQL | `/tmp/mysql.sock`, `/var/run/mysqld/mysqld.sock` | `/tmp/mysql.sock` |
| `UPLOAD_FOLDER` | Directorio para fotos subidas | `static/uploads`, `/var/www/uploads` | `static/uploads` |
| `MAX_CONTENT_LENGTH` | Tamaño máximo de archivo (bytes) | `16777216` (16MB) | `16777216` |
| `TEST_DATABASE_URL` | BD específica para testing | `sqlite:///:memory:` | `sqlite:///:memory:` |

### 💡 **Ejemplos de Configuración por Entorno**

#### **🏠 Desarrollo Local Básico (.env)**
```bash
FLASK_ENV=development
SECRET_KEY=dev-key-12345
DB_HOST=localhost
DB_USER=cc5002
DB_PASSWORD=programacionweb
DB_NAME=tarea2
```

#### **🐳 Docker Compose (.env)**
```bash
FLASK_ENV=development
SECRET_KEY=docker-dev-key
DB_HOST=mysql-container
DB_PORT=3306
DB_USER=cc5002
DB_PASSWORD=programacionweb
DB_NAME=tarea2
```

#### **☁️ Producción Heroku (.env)**
```bash
FLASK_ENV=production
SECRET_KEY=${HEROKU_SECRET_KEY}
DATABASE_URL=${CLEARDB_DATABASE_URL}
UPLOAD_FOLDER=/tmp/uploads
```

#### **🧪 Testing (.env.test)**
```bash
FLASK_ENV=testing
SECRET_KEY=test-key-not-secret
TEST_DATABASE_URL=sqlite:///test.db
UPLOAD_FOLDER=/tmp/test_uploads
```

## 🌐 URLs Disponibles

| Ruta | Descripción | Funcionalidad |
|------|-------------|---------------|
| `/` | **Portada** | Últimos 5 avisos de adopción |
| `/agregar-aviso` | **Formulario** | Publicar nuevo aviso con validación |
| `/listado-avisos` | **Listado** | Ver todos los avisos (paginado 5 por página) |
| `/estadisticas` | **Dashboard** | Gráficos y estadísticas del portal |

## 🆘 Solución de Problemas Comunes

### ❌ **Error: "Address already in use - Port 5000"**
```bash
# Solución: La app usa puerto 5001 por defecto
# Si necesitas cambiar el puerto, editar en app.py:
# app.run(debug=True, port=OTRO_PUERTO)
```

### ❌ **Error: "Can't connect to MySQL server"**
```bash
# Verificar que MySQL esté corriendo
sudo systemctl status mysql    # Linux
brew services list | grep mysql    # Mac

# Para Docker:
docker ps | grep mysql

# Para devbox:
devbox services status
```

### ❌ **Error: "No such file or directory: static/uploads"**
```bash
# El directorio se crea automáticamente al ejecutar
# Si persiste el error, crear manualmente:
mkdir -p static/uploads
chmod 755 static/uploads
```

### ❌ **Error: "Access denied for user 'cc5002'"**
```bash
# Verificar credenciales en .env
# Recrear usuario MySQL:
mysql -u root -p -e "DROP USER IF EXISTS 'cc5002'@'localhost';"
mysql -u root -p -e "CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';"
```

### ❌ **Error: "No module named 'app'"**
```bash
# Verificar que estés en el directorio correcto
cd desarrollo_web_Gabriel_Gallardo

# Verificar que el entorno virtual esté activo
source .venv/bin/activate

# Verificar instalación de dependencias
pip install -r requirements.txt
```

### ❌ **Error: "Table 'tarea2.aviso_adopcion' doesn't exist"**
```bash
# Importar estructura de base de datos
mysql -u cc5002 -p tarea2 < data/tarea2.sql
mysql -u cc5002 -p tarea2 < data/region-comuna.sql

# Verificar que las tablas se crearon
mysql -u cc5002 -p tarea2 -e "SHOW TABLES;"
```

## 🎯 Estado del Proyecto

- ✅ **Tarea 2 COMPLETA**: Todos los requerimientos implementados
- ✅ **Configuración Portable**: Sin variables hardcodeadas
- ✅ **Validación Robusta**: Server-side completa
- ✅ **Base de Datos**: Correctamente normalizada y poblada
- ✅ **Frontend Funcional**: Templates responsive con navegación
- ✅ **Documentación Completa**: Guías detalladas de instalación
- 🎯 **LISTO PARA EVALUACIÓN ACADÉMICA**

---

### 📞 **Soporte y Contacto**

Para problemas específicos, verificar:
1. **Variables de entorno** correctamente configuradas en `.env`
2. **Base de datos** creada e importada correctamente
3. **Dependencias** instaladas según `requirements.txt`
4. **Permisos** de escritura en directorio `static/uploads`
5. **Puerto** 5001 disponible o cambiar en configuración

**🎉 ¡Aplicación lista para demostración y evaluación!** 🎉