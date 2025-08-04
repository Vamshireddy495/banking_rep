from sqlalchemy import Column, Integer, String, Float, ForeignKey, DataTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key = True, index = True)
    from_account_id = Column(Integer, ForeignKey('accounts.id'), nullable = True)
    to_account_id = Column(Integer, ForeignKey('accounts.id'), nullable= True)
    amount = Column(Float, default = 0.0, nullable = False)
    timestamp = Column(DataTime(timezone= True), server_default= func.now())
    
    from_account = relationship("Account",foreign_keys= [from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])