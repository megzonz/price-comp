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

def clear_old_data(category_name):
    with Session() as session:
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
            
def clean_price(price):
    if isinstance(price, (int, float)):
        return Decimal(str(price))
    elif isinstance(price, str):
        # Remove non-numeric characters and convert to Decimal
        return Decimal(''.join(filter(lambda x: x.isdigit() or x == '.', price)))
    else:
        raise ValueError(f"Unexpected price type: {type(price)}")

def insert_product(product_data):
    with Session() as session:
        try:
            # Check if store exists, if not insert it
            store = session.query(Store).filter(Store.name == product_data['store_name']).first()
            if not store:
                store = Store(
                    name=product_data['store_name'],
                    logo_url=product_data.get('logo_url')
                )
                session.add(store)
                session.flush()

            # Check if category exists, if not insert it
            category = session.query(Category).filter(Category.name == product_data['category_name']).first()
            if not category:
                category = Category(name=product_data['category_name'])
                session.add(category)
                session.flush()

            # Check if product already exists
            product = session.query(Product).filter(Product.name == product_data['name']).first()

            if product:
                # Update product details
                product.description = product_data.get('description', product.description)
                product.image_url = product_data.get('image_url', product.image_url)
                product.link_to_product = product_data.get('link_to_product', product.link_to_product)
                product.category_id = category.id
                print(f"Product {product_data['name']} updated in the database.")
            else:
                # Insert product into products table
                product = Product(
                    name=product_data['name'],
                    description=product_data.get('description'),
                    image_url=product_data['image_url'],
                    store_id=store.id,
                    category_id=category.id,
                    link_to_product=product_data.get('link_to_product')
                )
                session.add(product)
                session.flush()
                print(f"Product {product_data['name']} added to the database.")

            # Insert or update price in prices table
            price_entry = session.query(Price).filter(
                Price.product_id == product.id,
                Price.store_id == store.id
            ).first()

            try:
                cleaned_price = clean_price(product_data['price'])
            except ValueError as e:
                print(f"Error cleaning price for {product_data['name']}: {e}")
                return  # Skip price update if price cleaning fails

            if price_entry:
                price_entry.price = cleaned_price
                price_entry.scraped_at = datetime.datetime.utcnow()
                print(f"Price updated for product {product_data['name']}.")
            else:
                new_price = Price(
                    product_id=product.id,
                    store_id=store.id,
                    price=cleaned_price,
                    currency='EUR',
                    scraped_at=datetime.datetime.utcnow()
                )
                session.add(new_price)
                print(f"New price added for product {product_data['name']}.")

            # Commit transaction
            session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Error inserting product: {e}")
        finally:
            session.close()