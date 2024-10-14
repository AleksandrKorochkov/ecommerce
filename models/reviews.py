import os
import sys
sys.path.append(os.getcwd())
from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, TIMESTAMP, DateTime
from models import *
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Raview(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))   
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey("raiting.id"))
    comment = Column(String)
    comment_date = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    user = relationship("User", uselist=False ,back_populates='reviews')
    product = relationship("Product", uselist=False, back_populates='reviews')
    raiting = relationship("Raiting",uselist=False ,back_populates='reviews')
    
