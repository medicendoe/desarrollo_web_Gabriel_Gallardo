#!/usr/bin/env python3
"""
Aplicación Flask para Portal de Adopción de Mascotas
Desarrollado con arquitectura modular y buenas prácticas
"""

from app import create_app
import os

# Crear la aplicación usando el factory pattern
app = create_app()

if __name__ == '__main__':
    # Solo para desarrollo - en producción usar un servidor WSGI
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='127.0.0.1',
        port=port,
        debug=debug
    )