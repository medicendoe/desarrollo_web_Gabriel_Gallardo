import os
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_datetime(value):
    """Formatear fecha y hora para mostrar en templates"""
    if value is None:
        return ""
    return value.strftime('%d/%m/%Y %H:%M')

def format_date(value):
    """Formatear solo fecha para mostrar en templates"""
    if value is None:
        return ""
    return value.strftime('%d/%m/%Y')

def create_upload_folder(upload_path):
    """Crear carpeta de uploads si no existe"""
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    return upload_path

def validate_email(email):
    """Validación básica de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validación básica de teléfono chileno"""
    import re
    # Formato chileno: +569XXXXXXXX o 9XXXXXXXX
    pattern = r'^(\+?569|9)[0-9]{8}$'
    return re.match(pattern, phone) is not None