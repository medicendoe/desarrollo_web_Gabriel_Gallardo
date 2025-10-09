from datetime import datetime
from .. import db

class Region(db.Model):
    """Modelo para las regiones de Chile"""
    __tablename__ = 'region'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    
    # Relaciones
    comunas = db.relationship('Comuna', backref='region', lazy=True)
    
    def __repr__(self):
        return f'<Region {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }

class Comuna(db.Model):
    """Modelo para las comunas de Chile"""
    __tablename__ = 'comuna'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    
    # Relaciones
    avisos = db.relationship('AvisoAdopcion', backref='comuna', lazy=True)
    
    def __repr__(self):
        return f'<Comuna {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'region_id': self.region_id
        }