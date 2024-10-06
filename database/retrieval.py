# database/retrieval.py
from sqlalchemy.orm import sessionmaker
from database.models import Product, Store, Price, Category
from database.database import get_db_connection

def get_all_products():
    Session = sessionmaker(bind=get_db_connection())
    session = Session()
    
    try:
        products = session.query(Product).all()
        result = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'image_url': product.image_url,
                'store_name': product.store.name,
                'category_name': product.category.name,
                'prices': [{'price': price.price, 'currency': price.currency} for price in product.prices]
            }
            result.append(product_data)
        return result
    
    finally:
        session.close()
