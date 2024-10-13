from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.endpoints.search import ProductDetailResponse, get_db
from database.models import Store, Product, Price, ProductStoreLink, Session as DBSession
from typing import List

router = APIRouter()

@router.get("/product/{product_id}/offers", response_model=ProductDetailResponse)
def get_product_offers(product_id: int, db: Session = Depends(get_db)):
    # Fetch product details with offers
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    offers = (
        db.query(
            Store.name.label('store_name'),
            Price.price,
            ProductStoreLink.link_to_product
        )
        .join(ProductStoreLink, ProductStoreLink.product_id == Product.id)
        .join(Price, ProductStoreLink.id == Price.product_store_link_id)
        .join(Store, ProductStoreLink.store_id == Store.id)
        .filter(Product.id == product_id)
        .all()
    )

    return {
        "name": product.name,
        "image_url": product.image_url,
        "offers": [
            {
                "store_name": offer.store_name,
                "price": float(offer.price),
                "link_to_product": offer.link_to_product
            }
            for offer in offers
        ]
    }
