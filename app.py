#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Flask de adopción de mascotas
"""

from app import create_app

# Crear la aplicación Flask usando el factory pattern
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)