from sqlalchemy.orm import subqueryload
from database.models import Product, Store, Price, ProductStoreLink, Category
from database.models import Session

def get_all_products():
    session = Session()

    try:
        # Query all products with related store, category, product links, and prices using subqueryload
        products = (
            session.query(Product)
            .options(
                subqueryload(Product.product_store_links).subqueryload(ProductStoreLink.store),
                subqueryload(Product.product_store_links).subqueryload(ProductStoreLink.prices),
                subqueryload(Product.category)  # Load the category for each product
            )
            .all()
        )

        result = []
        for product in products:
            for product_store_link in product.product_store_links:
                store = product_store_link.store
                prices = product_store_link.prices
                
                price_data = [{'price': float(price.price), 'scraped_at': price.scraped_at.isoformat()} for price in prices]

                product_data = {
                    'id': product.id,
                    'name': product.name,
                    'image_url': product.image_url,
                    'store_name': store.name,
                    'store_logo_url': store.logo_url,
                    'category_name': product.category.category_url,  # Assuming category_url is the key
                    'link_to_product': product_store_link.link_to_product,
                    'prices': price_data
                }
                result.append(product_data)

        return result

    finally:
        session.close()
