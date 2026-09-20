from flask import Blueprint, jsonify
from models.category import Category

bp = Blueprint('categories', __name__)

@bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    res = []
    for cat in categories:
        res.append({'id': cat.id, 'name': cat.name})
    return jsonify(res)
