from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel
from database.models import Product, Price, ProductStoreLink, Store
from api.endpoints.search import get_db

router = APIRouter()

class AutocompleteResponse(BaseModel):
    id: int
    name: str
    image_url: str
    price: float

@router.get("/autocomplete", response_model=List[AutocompleteResponse])
def autocomplete_products(query: str, db: Session = Depends(get_db)):
    try:
        results = (
            db.query(
                Product.id,
                Product.name,
                Product.image_url,
                func.min(Price.price).label('price')
            )
            .join(ProductStoreLink, ProductStoreLink.product_id == Product.id)
            .join(Price, ProductStoreLink.id == Price.product_store_link_id)
            .filter(Product.name.ilike(f"%{query}%"))
            .group_by(Product.id)
            .order_by(func.min(Price.price).asc())
            .limit(10)  # Limit results for autocomplete
            .all()
        )

        return [
            {
                "id": result.id,
                "name": result.name,
                "image_url": result.image_url,
                "price": float(result.price)
            }
            for result in results
        ]

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
