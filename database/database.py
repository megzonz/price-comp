from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    normalized_name = Column(String, index=True)
    prices = relationship('Price', back_populates='product')


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    retailer = Column(String)  
    price = Column(Float)  
    url = Column(String)  
    product = relationship('Product', back_populates='prices')
