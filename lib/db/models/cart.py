from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.models.supplement import Supplement
from db.models.user import User

Base = declarative_base()

class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    supplement_id = Column(Integer, ForeignKey('supplements.id'))
    quantity = Column(Integer, default=1)

    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, supplement_id={self.supplement_id}, quantity={self.quantity})"