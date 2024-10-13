from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Store, Product, Price, ProductStoreLink, Session as DBSession
from typing import List
from pydantic import BaseModel

router = APIRouter()

class OfferResponse(BaseModel):
    store_name: str
    price: float
    link_to_product: str

class ProductDetailResponse(BaseModel):
    name: str
    image_url: str
    offers: List[OfferResponse]

# Dependency to get a DB session
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/search", response_model=List[ProductDetailResponse])
def search_products(query: str, db: Session = Depends(get_db)):
    try:
        query_parts = query.split()
        base_query = (
            db.query(
                Product.id,  # Add product id here
                Product.name,
                Product.image_url,
                Store.name.label('store_name'),
                Store.logo_url.label('store_logo_url'),
                func.min(Price.price).label('price'),
                ProductStoreLink.link_to_product
            )
            .join(ProductStoreLink, ProductStoreLink.product_id == Product.id)
            .join(Price, ProductStoreLink.id == Price.product_store_link_id)
            .join(Store, ProductStoreLink.store_id == Store.id)
        )

        for part in query_parts:
            base_query = base_query.filter(Product.name.ilike(f"%{part}%"))

        results = base_query.group_by(Product.id, Store.id, ProductStoreLink.id).order_by(func.min(Price.price).asc()).all()

        if not results:
            return []

        products = {}
        for result in results:
            product_id = result.id  # Capture the product id here
            if product_id not in products:
                products[product_id] = {
                    "id": product_id,  # Add the id here
                    "name": result.name,
                    "image_url": result.image_url,
                    "offers": []
                }
            products[product_id]["offers"].append({
                "store_name": result.store_name,
                "price": float(result.price),
                "link_to_product": result.link_to_product
            })

        return list(products.values())

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
