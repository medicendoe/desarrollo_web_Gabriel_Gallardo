"""
Configuraciones de la aplicación Flask - Completamente parametrizables
Todas las configuraciones se obtienen de variables de entorno para máxima portabilidad
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    """Configuración base de la aplicación - Valores por defecto seguros"""
    
    # Clave secreta - SIEMPRE cambiar en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLAlchemy - Configuración general
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para subida de archivos - Completamente parametrizable
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB por defecto
    
    # Parámetros de base de datos - Sin valores hardcodeados
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'cc5002')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'programacionweb')
    DB_NAME = os.environ.get('DB_NAME', 'tarea2')

class DevelopmentConfig(Config):
    """
    Configuración para desarrollo - Adaptable a cualquier entorno
    Soporta tanto conexiones TCP estándar como socket Unix
    """
    DEBUG = True
    
    # Determinar método de conexión según variables de entorno
    if os.environ.get('USE_UNIX_SOCKET', '').lower() == 'true':
        # Para entornos con socket Unix (Docker, devbox, etc.)
        socket_path = os.environ.get('MYSQL_UNIX_SOCKET', '/tmp/mysql.sock')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}?unix_socket={socket_path}'
    else:
        # Conexión TCP estándar - Compatible con cualquier instalación MySQL
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'

class ProductionConfig(Config):
    """
    Configuración para producción - Segura y flexible
    Prioriza DATABASE_URL completa, con fallback a componentes individuales
    """
    DEBUG = False
    
    # Preferir DATABASE_URL completa (común en servicios cloud)
    # Fallback a construcción desde componentes individuales
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'

class TestConfig(Config):
    """
    Configuración para testing - Aislada y rápida
    Por defecto usa SQLite en memoria para velocidad
    """
    TESTING = True
    DEBUG = True
    
    # SQLite en memoria para tests rápidos, configurable para tests de integración
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')

# Mapeo de configuraciones - Selección automática según FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig  # Fallback seguro para desarrollo
}