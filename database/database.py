import datetime
from decimal import Decimal
from database.models import Session, Store, Category, Product, Price
import psycopg2
from psycopg2 import sql
import os

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),  
            user=os.getenv("DB_USER"),    
            password=os.getenv("DB_PASS"), 
            host=os.getenv("DB_HOST"),    
            port=os.getenv("DB_PORT")      
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def insert_product(product_data):
    """
    Inserts a product into the database. It first checks if the store and category exist,
    and inserts them if not. Then, it adds the product and its price in the appropriate tables.
    """
    session = Session()

    # Check if the store exists, if not, insert it
    store = session.query(Store).filter_by(name=product_data['store_name']).first()
    if not store:
        store = Store(name=product_data['store_name'], logo_url=product_data['logo_url'])
        session.add(store)
        session.commit()

    # Check if the category exists, if not, insert it
    category = session.query(Category).filter_by(category_url=product_data['category_name']).first()
    if not category:
        category = Category(category_url=product_data['category_name'])
        session.add(category)
        session.commit()

    # Check if the product exists (optional: if you need to avoid duplicate product names)
    existing_product = session.query(Product).filter_by(name=product_data['name'], store_id=store.id).first()
    if not existing_product:
        # Insert the product into the database
        product = Product(
            name=product_data['name'],
            image_url=product_data['image_url'],
            link_to_product=product_data['link_to_product'],
            store_id=store.id,
            category_id=category.id
        )
        session.add(product)
        session.commit()
    else:
        product = existing_product  # If the product already exists, we don't insert it again

    # Insert the product price into the Price table
    price_entry = Price(
        product_id=product.id,
        price=Decimal(product_data['price']),
        scraped_at=datetime.datetime.utcnow()  # Automatically use the current time for scraped_at
    )

    session.add(price_entry)
    session.commit()
    session.close()

    print(f"Product '{product_data['name']}' with price {product_data['price']} inserted into the database.")

