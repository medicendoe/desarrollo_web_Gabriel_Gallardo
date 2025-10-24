from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import config
import os

# Instancias de extensiones
db = SQLAlchemy()

def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configuración
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    from .routes.main import main_bp
    from .routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app