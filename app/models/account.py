from sqlalchemy import  Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Float, default = 0.0)
    account_type = Column(String(50))

    owner = relationship('User', back_populates = 'accounts')