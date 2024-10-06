import datetime
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

def clear_old_data(category_name):
    session = Session()
    try:
        # Delete prices associated with the category
        session.query(Price).filter(Price.product_id.in_(
            session.query(Product.id).join(Category).filter(Category.name == category_name)
        )).delete(synchronize_session=False)

        # Optionally, delete products that no longer have prices
        session.query(Product).filter(~Product.id.in_(session.query(Price.product_id))).delete(synchronize_session=False)

        print(f"Old data cleared for category: {category_name}")
        session.commit()
    
    except Exception as e:
        session.rollback()
        print(f"Error clearing old data: {e}")
    
    finally:
        session.close()

def insert_product(product_data):
    session = Session()
    try:
        # Check if store exists, if not insert it
        store = session.query(Store).filter(Store.name == product_data['store_name']).first()
        if not store:
            store = Store(name=product_data['store_name'], logo_url=product_data['logo_url'], link_to_product=product_data['link_to_product'])
            session.add(store)
            session.commit()

        # Check if category exists, if not insert it
        category = session.query(Category).filter(Category.name == product_data['category_name']).first()
        if not category:
            category = Category(name=product_data['category_name'])
            session.add(category)
            session.commit()

        # Check if product already exists
        product = session.query(Product).filter(Product.name == product_data['name']).first()

        if product:
            # Update product price if it exists
            price_entry = session.query(Price).filter(Price.product_id == product.id, Price.store_id == store.id).first()
            if price_entry:
                price_entry.price = product_data['price']
                price_entry.scraped_at = datetime.datetime.utcnow()
                print(f"Product {product_data['name']} updated in the database.")
            else:
                new_price = Price(product_id=product.id, store_id=store.id, price=product_data['price'], currency='EUR')
                session.add(new_price)
                print(f"New price added for product {product_data['name']}.")
        else:
            # Insert product into products table
            product = Product(name=product_data['name'], image_url=product_data['image_url'], store_id=store.id, category_id=category.id)
            session.add(product)
            session.commit()

            # Insert price into prices table
            new_price = Price(product_id=product.id, store_id=store.id, price=product_data['price'], currency='EUR')
            session.add(new_price)
            print(f"Product {product_data['name']} added to the database.")

        # Commit transaction
        session.commit()
    
    except Exception as e:
        session.rollback()
        print(f"Error inserting product: {e}")
    finally:
        session.close()
