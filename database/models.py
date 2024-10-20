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

    offers = relationship("Offer", back_populates="store")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_url = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    base_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")
    offers = relationship("Offer", back_populates="product")

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    name = Column(String, nullable=False)
    image_url = Column(String)
    link_to_product = Column(String, nullable=False)

    product = relationship("Product", back_populates="offers")
    store = relationship("Store", back_populates="offers")
    prices = relationship("Price", back_populates="offer")

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)

    offer = relationship("Offer", back_populates="prices")

# Database connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    """
    Function to create the necessary database tables.
    """
    Base.metadata.create_all(engine)
    print("Tables created or already exist.")