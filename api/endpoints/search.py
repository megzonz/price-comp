from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Store, Product, Price, Category, Session as DBSession
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Updated Pydantic model for the response
class ProductResponse(BaseModel):
    name: str
    image_url: str
    store_logo_url: str 
    price: float
    link_to_product: str

class SearchResponse(BaseModel):
    products: List[ProductResponse]

# Dependency to get a DB session
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/search", response_model=SearchResponse)
def search_products(query: str, db: Session = Depends(get_db)):
    # Split the query into individual words
    query_parts = query.split()

    # Start building the query
    base_query = (
        db.query(
            Product.name,
            Product.image_url,
            Store.logo_url.label('store_logo_url'),
            func.min(Price.price).label('price'),
            Product.link_to_product
        )
        .join(Price, Product.id == Price.product_id)
        .join(Store, Price.store_id == Store.id)
    )

    # Add filters for each part of the query
    for part in query_parts:
        base_query = base_query.filter(Product.name.ilike(f"%{part}%"))

    # Group by product and store and order by price
    products = (
        base_query
        .group_by(Product.id, Store.id)
        .order_by(func.min(Price.price).asc())
        .all()
    )

    if not products:
        return {"products": []}

    # Format the response
    result = [
        {
            "name": product.name,
            "image_url": product.image_url,
            "store_logo_url": product.store_logo_url,
            "price": float(product.price),
            "link_to_product": product.link_to_product
        }
        for product in products
    ]

    return {"products": result}