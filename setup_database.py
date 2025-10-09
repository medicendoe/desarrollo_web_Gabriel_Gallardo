#!/usr/bin/env python3
"""
Script para inicializar la base de datos con la estructura y datos iniciales.
Ejecutar este script antes de usar la aplicación Flask.
"""

import sys
import os
from sqlalchemy import create_engine, text
from app import db, app

def ejecutar_script_sql(engine, archivo_sql):
    """Ejecuta un archivo SQL línea por línea"""
    print(f"Ejecutando {archivo_sql}...")
    
    with open(archivo_sql, 'r', encoding='utf-8') as file:
        contenido = file.read()
    
    # Dividir en comandos SQL individuales
    comandos = contenido.split(';')
    
    with engine.connect() as connection:
        for comando in comandos:
            comando = comando.strip()
            if comando and not comando.startswith('--'):
                try:
                    connection.execute(text(comando))
                    connection.commit()
                except Exception as e:
                    print(f"Error ejecutando comando: {comando[:50]}...")
                    print(f"Error: {e}")
                    # Continuar con el siguiente comando
                    pass

def setup_database():
    """Configura la base de datos completa"""
    print("Configurando la base de datos...")
    
    # Usar socket Unix para conexión local con devbox
    socket_path = "/Users/doe/Personal/daw/.devbox/virtenv/mysql/run/mysql.sock"
    
    # Crear engine para conectar a MySQL sin especificar la base de datos
    engine_root = create_engine(f'mysql+pymysql://cc5002:programacionweb@localhost/?unix_socket={socket_path}')
    
    # Crear la base de datos tarea2 si no existe
    with engine_root.connect() as connection:
        try:
            connection.execute(text("CREATE DATABASE IF NOT EXISTS tarea2 CHARACTER SET utf8"))
            connection.commit()
            print("Base de datos 'tarea2' creada o ya existe.")
        except Exception as e:
            print(f"Error creando la base de datos: {e}")
            return False
    
    # Crear engine para la base de datos específica
    engine = create_engine(f'mysql+pymysql://cc5002:programacionweb@localhost/tarea2?unix_socket={socket_path}')
    
    # Ejecutar script de estructura
    archivo_estructura = 'data/tarea2.sql'
    if os.path.exists(archivo_estructura):
        ejecutar_script_sql(engine, archivo_estructura)
        print("Estructura de la base de datos creada.")
    else:
        print(f"Archivo {archivo_estructura} no encontrado.")
        return False
    
    # Ejecutar script de datos iniciales
    archivo_datos = 'data/region-comuna.sql'
    if os.path.exists(archivo_datos):
        ejecutar_script_sql(engine, archivo_datos)
        print("Datos iniciales de regiones y comunas cargados.")
    else:
        print(f"Archivo {archivo_datos} no encontrado.")
        return False
    
    print("¡Base de datos configurada exitosamente!")
    return True

def verificar_conexion():
    """Verifica que la conexión a la base de datos funcione"""
    try:
        with app.app_context():
            # Verificar conexión
            from app import Region, Comuna
            total_regiones = Region.query.count()
            total_comunas = Comuna.query.count()
            
            print(f"Conexión exitosa. Regiones: {total_regiones}, Comunas: {total_comunas}")
            return True
    except Exception as e:
        print(f"Error verificando la conexión: {e}")
        return False

if __name__ == '__main__':
    print("Iniciando configuración de la base de datos...")
    print("Credenciales: host=localhost, puerto=3306, db=tarea2, user=cc5002")
    
    # Verificar que los archivos SQL existan
    archivos_necesarios = ['data/tarea2.sql', 'data/region-comuna.sql']
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            print(f"ERROR: Archivo {archivo} no encontrado.")
            sys.exit(1)
    
    # Configurar base de datos
    if setup_database():
        print("\nVerificando la configuración...")
        if verificar_conexion():
            print("\n✅ ¡Configuración completada exitosamente!")
            print("\nAhora puedes ejecutar la aplicación Flask con:")
            print("python app.py")
        else:
            print("\n❌ Error en la verificación de la conexión.")
            sys.exit(1)
    else:
        print("\n❌ Error en la configuración de la base de datos.")
        sys.exit(1)