import os
import sys
sys.path.append(os.getcwd())
from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from models import *

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    rating = Column(Float)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="product")
    reviews = relationship("Raview", back_populates="product") 
    raiting = relationship('Raiting', back_populates='product')
