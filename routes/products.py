from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models.product import Product
from models.category import Category

bp = Blueprint('products', __name__)

@bp.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('home.html', categories=categories, products=products)

@bp.route('/api/products/search')
def search():
    q = request.args.get('q', '').lower()
    products = Product.query.filter(Product.name.ilike(f'%{q}%')).all()
    
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'category': p.category.name,
            'image_url': p.image_url
        })
    return jsonify(result)
