from fuzzywuzzy import fuzz
from decimal import Decimal
from sqlalchemy.orm import Session
from database.models import Store, Product, ProductStoreLink, Price
import datetime

def insert_or_map_product(product_data, db: Session):
    """
    Inserts or maps a product from a new store (e.g., 75Mall) to an existing product in the database.
    If the product already exists (based on name matching), we add a new entry in ProductStoreLink and Price.
    """
    # First, check if the store exists, if not, insert it
    store = db.query(Store).filter_by(name=product_data['store_name']).first()
    if not store:
        store = Store(name=product_data['store_name'], logo_url=product_data['logo_url'])
        db.add(store)
        db.commit()

    # Fetch all products from the database for fuzzy matching
    all_products = db.query(Product).all()

    # Try to find a product match in the existing database using fuzzy matching
    matched_product = None
    for product in all_products:
        # Adjust the threshold as per your needs (e.g., 80 for less strict matching, 90 for more strict)
        similarity_ratio = fuzz.ratio(product.name.lower(), product_data['name'].lower())
        if similarity_ratio > 85:  # If we find a close match, we use this product
            matched_product = product
            break

    if matched_product:
        print(f"Matched product found: {matched_product.name}")
    else:
        # If no match is found, create a new product entry
        matched_product = Product(
            name=product_data['name'],
            image_url=product_data['image_url'],
            category_id=product_data['category_id']
        )
        db.add(matched_product)
        db.commit()

    # Now we link this product with the new store and insert the price
    product_store_link = (
        db.query(ProductStoreLink)
        .filter_by(product_id=matched_product.id, store_id=store.id)
        .first()
    )

    if not product_store_link:
        # Create a new product-store link if it doesn't exist
        product_store_link = ProductStoreLink(
            product_id=matched_product.id,
            store_id=store.id,
            link_to_product=product_data['link_to_product']
        )
        db.add(product_store_link)
        db.commit()

    # Insert the product price for this store
    price_entry = Price(
        product_store_link_id=product_store_link.id,
        price=Decimal(product_data['price']),
        scraped_at=datetime.datetime.utcnow()
    )
    db.add(price_entry)
    db.commit()

    print(f"Product '{product_data['name']}' with price {product_data['price']} added for store '{store.name}'")
