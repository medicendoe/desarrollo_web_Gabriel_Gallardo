from datetime import datetime
from .. import db

class AvisoAdopcion(db.Model):
    """Modelo para los avisos de adopción"""
    __tablename__ = 'aviso_adopcion'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'), nullable=False)
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    tipo = db.Column(db.Enum('gato', 'perro', name='tipo_mascota'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Enum('a', 'm', name='unidad_medida'), nullable=False)  # 'a' años, 'm' meses
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    fotos = db.relationship('Foto', foreign_keys='Foto.actividad_id', backref='aviso', lazy=True, cascade='all, delete-orphan')
    contactos = db.relationship('ContactarPor', foreign_keys='ContactarPor.actividad_id', backref='aviso', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AvisoAdopcion {self.nombre} - {self.tipo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'comuna_id': self.comuna_id,
            'sector': self.sector,
            'nombre': self.nombre,
            'email': self.email,
            'celular': self.celular,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'edad': self.edad,
            'unidad_medida': self.unidad_medida,
            'fecha_entrega': self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            'descripcion': self.descripcion
        }

class Foto(db.Model):
    """Modelo para las fotos de los avisos"""
    __tablename__ = 'foto'
    
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)
    
    def __repr__(self):
        return f'<Foto {self.nombre_archivo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ruta_archivo': self.ruta_archivo,
            'nombre_archivo': self.nombre_archivo,
            'actividad_id': self.actividad_id
        }

class ContactarPor(db.Model):
    """Modelo para las formas de contacto"""
    __tablename__ = 'contactar_por'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra', name='nombre_contacto'), nullable=False)
    identificador = db.Column(db.String(150), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)
    
    def __repr__(self):
        return f'<ContactarPor {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'identificador': self.identificador,
            'actividad_id': self.actividad_id
        }