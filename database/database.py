from fuzzywuzzy import fuzz
from decimal import Decimal
from sqlalchemy.orm import Session
from database.models import Store, Product, Offer, Price
import datetime

def extract_base_name(full_name):
    """
    Extracts the base name of a product (before the first comma).
    """
    return full_name.split(',')[0].strip()

def insert_or_map_product(product_data, db: Session):
    """
    Inserts or maps a product from a new store (e.g., 75Mall) to an existing product in the database.
    If the product already exists (based on base_name matching), we add a new entry in Offer and Price.
    """
    # First, check if the store exists, if not, insert it
    store = db.query(Store).filter_by(name=product_data['store_name']).first()
    if not store:
        store = Store(name=product_data['store_name'], logo_url=product_data['logo_url'])
        db.add(store)
        db.commit()

    # Extract the base name from the incoming product
    incoming_base_name = extract_base_name(product_data['name'])

    # Fetch all products from the database for base_name matching
    matched_product = db.query(Product).filter_by(base_name=incoming_base_name).first()

    if matched_product:
        print(f"Matched base product found: {matched_product.base_name}")
    else:
        # If no match is found, create a new product entry
        matched_product = Product(
            base_name=incoming_base_name,  # Save the base name
            category_id=product_data['category_id']  # Assuming category ID is part of the product_data
        )
        db.add(matched_product)
        db.commit()

    # Now we link this product with the new store and insert the offer, ensuring full product variations are saved
    # We use both the product name and the store to avoid overwriting offers for variations (e.g., 512GB vs. 1TB)
    offer = (
        db.query(Offer)
        .filter_by(product_id=matched_product.id, store_id=store.id, name=product_data['name'])
        .first()
    )

    if not offer:
        # Create a new offer if it doesn't exist, even for variations (e.g., 512GB, 1TB)
        offer = Offer(
            product_id=matched_product.id,
            store_id=store.id,
            name=product_data['name'],  # Save the full name for this offer, including storage and color variations
            image_url=product_data['image_url'],  # Store-specific image
            link_to_product=product_data['link_to_product']
        )
        db.add(offer)
        db.commit()

    # Insert the product price for this offer
    price_entry = Price(
        offer_id=offer.id,
        price=Decimal(product_data['price']),
        scraped_at=datetime.datetime.utcnow()
    )
    db.add(price_entry)
    db.commit()

    print(f"Product '{product_data['name']}' with price {product_data['price']} added for store '{store.name}'")