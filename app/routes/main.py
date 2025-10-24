from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .. import db
from ..models import Region, Comuna, AvisoAdopcion, Foto, ContactarPor
from datetime import datetime
import os
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal - Muestra los últimos 5 avisos de adopción"""
    # Obtener los últimos 5 avisos de adopción ordenados por fecha
    ultimos_avisos = AvisoAdopcion.query.order_by(
        AvisoAdopcion.fecha_ingreso.desc()
    ).limit(5).all()
    
    return render_template('index.html', avisos=ultimos_avisos)

@main_bp.route('/agregar-aviso', methods=['GET', 'POST'])
def agregar_aviso():
    """Página para agregar un nuevo aviso de adopción con validación del servidor"""
    # Cargar regiones para el formulario
    regiones = Region.query.all()
    
    if request.method == 'POST':
        # Obtener datos del formulario según los nombres reales en el template
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        celular = request.form.get('celular', '').strip()
        
        # Información del lugar
        region_id = request.form.get('region', '')
        comuna_id = request.form.get('comuna', '')
        sector = request.form.get('sector', '').strip()
        
        # Información de la mascota
        tipo = request.form.get('tipo', '')
        descripcion = request.form.get('descripcion', '').strip()
        fecha_entrega = request.form.get('fecha-entrega', '')
        cantidad_str = request.form.get('cantidad', '1')
        edad_str = request.form.get('edad', '1')
        
        # Validaciones del servidor
        errors = []
        
        # Validar campos obligatorios
        if not nombre:
            errors.append('El nombre es obligatorio')
        if not email:
            errors.append('El email es obligatorio')
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('El email debe tener formato válido')
        if not comuna_id:
            errors.append('Debe seleccionar una comuna')
        if not tipo:
            errors.append('Debe seleccionar un tipo de animal')
        if not descripcion:
            errors.append('La descripción es obligatoria')
        if not fecha_entrega:
            errors.append('Debe especificar una fecha de entrega')
        
        # Validar cantidad como número entero
        try:
            cantidad = int(float(cantidad_str))
            if cantidad < 1 or cantidad > 20:
                errors.append('La cantidad debe ser un número entero entre 1 y 20')
        except (ValueError, TypeError):
            errors.append('La cantidad debe ser un número entero válido')
            cantidad = 1
        
        # Validar edad como número entero
        try:
            edad = int(float(edad_str))
            if edad < 1:
                errors.append('La edad debe ser un número mayor a 0')
        except (ValueError, TypeError):
            errors.append('La edad debe ser un número entero válido')
            edad = 1
        
        # Validar que haya al menos un medio de contacto
        contactos_adicionales_nombres = request.form.getlist('contacto_nombre[]')
        contactos_adicionales_ids = request.form.getlist('contacto_id[]')
        
        has_valid_contact = email or celular
        
        # Verificar contactos adicionales válidos
        for i, (nombre_contacto, id_contacto) in enumerate(zip(contactos_adicionales_nombres, contactos_adicionales_ids)):
            if nombre_contacto and id_contacto.strip():
                has_valid_contact = True
                break
        
        if not has_valid_contact:
            errors.append('Debe proporcionar al menos un medio de contacto válido')
        
        # Si hay errores, mostrarlos
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('agregar_aviso.html', regiones=regiones)
        
        # Si no hay errores, procesar el formulario
        try:
            # Convertir fecha de entrega
            fecha_entrega_dt = datetime.strptime(fecha_entrega, '%Y-%m-%dT%H:%M') if 'T' in fecha_entrega else datetime.strptime(fecha_entrega, '%Y-%m-%d')
            
            # Crear nuevo aviso
            nuevo_aviso = AvisoAdopcion(
                comuna_id=int(comuna_id),
                sector=sector or None,
                nombre=nombre,
                email=email,
                celular=celular or None,
                tipo=tipo,
                cantidad=cantidad,
                edad=edad,
                unidad_medida=request.form.get('unidad-edad', 'm'),
                fecha_entrega=fecha_entrega_dt,
                descripcion=descripcion,
                fecha_ingreso=datetime.now()
            )
            
            db.session.add(nuevo_aviso)
            db.session.flush()  # Para obtener el ID
            
            # Agregar contacto por email (siempre presente por validación)
            if email:
                contacto_email = ContactarPor(
                    actividad_id=nuevo_aviso.id,
                    nombre='otra',  # Usar 'otra' para email
                    identificador=f"Email: {email}"
                )
                db.session.add(contacto_email)
            
            # Agregar contacto por celular si está presente
            if celular:
                contacto_celular = ContactarPor(
                    actividad_id=nuevo_aviso.id,
                    nombre='otra',  # Usar 'otra' para celular
                    identificador=f"Celular: {celular}"
                )
                db.session.add(contacto_celular)
            
            # Agregar contactos adicionales
            for i, (nombre_contacto, id_contacto) in enumerate(zip(contactos_adicionales_nombres, contactos_adicionales_ids)):
                if nombre_contacto and id_contacto.strip():
                    contacto_adicional = ContactarPor(
                        actividad_id=nuevo_aviso.id,
                        nombre=nombre_contacto,
                        identificador=id_contacto.strip()
                    )
                    db.session.add(contacto_adicional)
            
            # Manejar archivos de foto
            fotos = request.files.getlist('fotos')
            for foto in fotos:
                if foto and foto.filename:
                    # Generar nombre único para el archivo
                    filename = secure_filename(foto.filename)
                    if filename:
                        # Crear directorio de uploads si no existe
                        upload_dir = os.path.join(current_app.static_folder, 'uploads')
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        # Guardar archivo
                        ruta_archivo = os.path.join(upload_dir, filename)
                        foto.save(ruta_archivo)
                        
                        # Guardar info en BD (ruta relativa para web)
                        nueva_foto = Foto(
                            actividad_id=nuevo_aviso.id,
                            nombre_archivo=filename,
                            ruta_archivo=f'uploads/{filename}'
                        )
                        db.session.add(nueva_foto)
            
            # Confirmar transacción
            db.session.commit()
            
            flash('Aviso agregado correctamente', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar el aviso: {str(e)}', 'error')
            return render_template('agregar_aviso.html', regiones=regiones)
    
    return render_template('agregar_aviso.html', regiones=regiones)

@main_bp.route('/listado-avisos')
def listado_avisos():
    """Listado de todos los avisos de adopción - 5 por página"""
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Mostrar 5 avisos por página según requerimiento
    
    # Ordenar por fecha de ingreso descendente (más recientes primero)
    avisos = AvisoAdopcion.query.order_by(
        AvisoAdopcion.fecha_ingreso.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('listado_avisos.html', avisos=avisos)

@main_bp.route('/estadisticas')
def estadisticas():
    """Página de estadísticas"""
    try:
        # Estadísticas por tipo
        stats_tipo = db.session.query(
            AvisoAdopcion.tipo,
            db.func.count(AvisoAdopcion.id).label('total')
        ).group_by(AvisoAdopcion.tipo).all()
        
        # Estadísticas por región
        stats_region = db.session.query(
            Region.nombre,
            db.func.count(AvisoAdopcion.id).label('total')
        ).select_from(Region).join(
            Comuna, Region.id == Comuna.region_id
        ).join(
            AvisoAdopcion, Comuna.id == AvisoAdopcion.comuna_id
        ).group_by(Region.nombre).all()
        
        # Estadísticas por comuna (top 10)
        stats_comuna = db.session.query(
            Comuna.nombre,
            db.func.count(AvisoAdopcion.id).label('total')
        ).join(
            AvisoAdopcion, Comuna.id == AvisoAdopcion.comuna_id
        ).group_by(Comuna.nombre).order_by(
            db.func.count(AvisoAdopcion.id).desc()
        ).limit(10).all()
        
        return render_template('estadisticas.html', 
                             stats_tipo=stats_tipo,
                             stats_region=stats_region,
                             stats_comuna=stats_comuna)
    except Exception as e:
        flash(f'Error al cargar estadísticas: {str(e)}', 'error')
        return render_template('estadisticas.html', 
                             stats_tipo=[],
                             stats_region=[],
                             stats_comuna=[])