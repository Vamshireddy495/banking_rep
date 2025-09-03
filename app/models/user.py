from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, index = True, primary_key = True)
    email = Column(String(255), nullable = False, unique = True)
    full_name = Column(String(255), nullable = False)
    hashed_password = Column(String(255), nullable = False)
    is_active = Column(Boolean, default = True)
    is_admin = Column(Boolean, default = False)

    accounts = relationship('Account', back_populates = 'owner')

