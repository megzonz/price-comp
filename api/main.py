from fastapi import FastAPI
from api.endpoints import search, products
from database.database import engine
from database.models import Base

app = FastAPI(title="Kosovo Price Comparison API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Kosovo Price Comparison API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
