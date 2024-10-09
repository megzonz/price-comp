from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os

Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    logo_url = Column(String)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_url = Column(String, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String)
    link_to_product = Column(String)
    store_id = Column(Integer, ForeignKey('stores.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    # Define relationships
    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")
    prices = relationship("Price", back_populates="product")  # Link to prices

Store.products = relationship("Product", back_populates="store")
Category.products = relationship("Product", back_populates="category")

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Define relationship
    product = relationship("Product", back_populates="prices")

# Database connection
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    """
    Function to create the necessary database tables.
    """
    Base.metadata.create_all(engine)
    print("Tables created or already exist.")
