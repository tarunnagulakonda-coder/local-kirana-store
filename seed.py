import os
from werkzeug.security import generate_password_hash
from app import create_app
from models import db
# Ensure models are imported so SQLAlchemy knows about them
from models import user, category, product, cart, order, admin
from models.category import Category
from models.product import Product
from models.admin import Admin
from datetime import datetime

app = create_app()

def seed_data():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if admin exists
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin')
        if not Admin.query.filter_by(username=admin_username).first():
            new_admin = Admin(
                username=admin_username, 
                password_hash=generate_password_hash(admin_password)
            )
            db.session.add(new_admin)
        
        # Categories
        cat_names = [
            "Biriyani Uma", "Vegetables", "Fruits", "Beverages", 
            "Rice & Grains", "Pulses", "Spices", "Snacks", 
            "Dairy", "Household", "Personal Care"
        ]
        
        for name in cat_names:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))
        
        db.session.commit()
        
        # Products
        demo_products = [
            {"name": "Rice 5kg", "category": "Rice & Grains", "price": 350, "image": "rice.jpg"},
            {"name": "Wheat Flour 1kg", "category": "Rice & Grains", "price": 55, "image": "wheat.jpg"},
            {"name": "Toor Dal 1kg", "category": "Pulses", "price": 140, "image": "toor.jpg"},
            {"name": "Moong Dal 1kg", "category": "Pulses", "price": 120, "image": "moong.jpg"},
            {"name": "Chana Dal 1kg", "category": "Pulses", "price": 90, "image": "chana.jpg"},
            {"name": "Tomato 1kg", "category": "Vegetables", "price": 40, "image": "tomato.jpg"},
            {"name": "Potato 1kg", "category": "Vegetables", "price": 35, "image": "potato.jpg"},
            {"name": "Onion 1kg", "category": "Vegetables", "price": 45, "image": "onion.jpg"},
            {"name": "Carrot 1kg", "category": "Vegetables", "price": 60, "image": "carrot.jpg"},
            {"name": "Banana 1 Dozen", "category": "Fruits", "price": 60, "image": "banana.jpg"},
            {"name": "Apple 1kg", "category": "Fruits", "price": 150, "image": "apple.jpg"},
            {"name": "Milk 1L", "category": "Dairy", "price": 60, "image": "milk.jpg"},
            {"name": "Curd 500g", "category": "Dairy", "price": 40, "image": "curd.jpg"},
            {"name": "Tea Powder 250g", "category": "Beverages", "price": 120, "image": "tea.jpg"},
            {"name": "Coffee 100g", "category": "Beverages", "price": 90, "image": "coffee.jpg"},
            {"name": "Biscuits", "category": "Snacks", "price": 30, "image": "biscuits.jpg"},
            {"name": "Chips", "category": "Snacks", "price": 20, "image": "chips.jpg"},
            {"name": "Turmeric Powder 100g", "category": "Spices", "price": 35, "image": "turmeric.jpg"},
            {"name": "Chilli Powder 100g", "category": "Spices", "price": 40, "image": "chilli.jpg"},
            {"name": "Dish Wash 500ml", "category": "Household", "price": 80, "image": "dishwash.jpg"},
            {"name": "Biriyani Kit", "category": "Biriyani Uma", "price": 250, "image": "biriyani.jpg"}
        ]
        
        for p in demo_products:
            if not Product.query.filter_by(name=p['name']).first():
                cat = Category.query.filter_by(name=p['category']).first()
                if cat:
                    prod = Product(
                        name=p['name'],
                        category_id=cat.id,
                        price=p['price'],
                        image_url=p['image'],
                        expiry_date="31/12/2026",
                        description="High quality " + p['name']
                    )
                    db.session.add(prod)
        db.session.commit()
        print("Database seeding completed.")

if __name__ == '__main__':
    seed_data()
