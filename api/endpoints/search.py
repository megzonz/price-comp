from fastapi import APIRouter, Query
from database.database import get_db_connection  # Import your DB connection logic

router = APIRouter()

@router.get("/search")
def search_products(query: str):
    conn = get_db_connection()
    with conn.cursor() as cur:
        sql_query = """
            SELECT p.name, p.image_url, pr.price, pr.currency, s.name AS store_name, s.logo_url AS store_logo, s.link_to_product
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
            JOIN stores s ON pr.store_id = s.id
            WHERE p.name ILIKE %s
            ORDER BY pr.price ASC
        """
        params = [f"%{query}%"]

        cur.execute(sql_query, params)
        products = cur.fetchall()
        conn.close()

    return {
        "products": [
            {
                "name": product[0],
                "image_url": product[1],  
                "price": product[2], 
                "currency": product[3],  
                "store_name": product[4],  
                "store_logo": product[5],  
                "link_to_product": product[6], 
            }
            for product in products
        ]
    }
