import os
import sys
sys.path.append(os.getcwd())
from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, TIMESTAMP
from models import *
from sqlalchemy.orm import relationship


class Raiting(Base):
    __tablename__ = "raiting"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey('products.id'))
    is_active = Column(Boolean, default=True) 

    user = relationship("User" , uselist=False, back_populates='raiting')
    product = relationship('Product', uselist=False, back_populates='raiting')
    reviews = relationship("Raview", uselist=False, back_populates='raiting')