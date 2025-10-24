from flask import Blueprint, jsonify, request
from ..models import Region, Comuna, AvisoAdopcion

api_bp = Blueprint('api', __name__)

@api_bp.route('/comunas/<int:region_id>')
def get_comunas(region_id):
    """API endpoint para obtener comunas por región"""
    try:
        comunas = Comuna.query.filter_by(region_id=region_id).all()
        return jsonify([comuna.to_dict() for comuna in comunas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/aviso/<int:aviso_id>')
def get_aviso(aviso_id):
    """API endpoint para obtener detalles de un aviso"""
    try:
        aviso = AvisoAdopcion.query.get_or_404(aviso_id)
        return jsonify(aviso.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/regiones')
def get_regiones():
    """API endpoint para obtener todas las regiones"""
    try:
        regiones = Region.query.all()
        return jsonify([region.to_dict() for region in regiones])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/avisos')
def get_avisos():
    """API endpoint para obtener avisos con filtros opcionales"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        tipo = request.args.get('tipo')
        region_id = request.args.get('region_id', type=int)
        
        query = AvisoAdopcion.query
        
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        if region_id:
            query = query.join(Comuna).filter(Comuna.region_id == region_id)
        
        avisos = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'avisos': [aviso.to_dict() for aviso in avisos.items],
            'total': avisos.total,
            'pages': avisos.pages,
            'current_page': avisos.page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500