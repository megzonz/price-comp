from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints import search
from database.retrieval import get_all_products



app = FastAPI()

# Include the search router
app.include_router(search.router)

@app.get("/products")
def read_products():
    products = get_all_products()
    return products

# Serve the frontend (HTML, JS, CSS)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
