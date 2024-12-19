from db.models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.models.supplement import Supplement
from db.models.user import User


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, ForeignKey('users.id'))
    supplement_name = Column(String, ForeignKey('supplements.id'))
    supplement_price = Column(Float,)
    quantity = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  
    supplement_id = Column(Integer, ForeignKey('supplements.id'), nullable=False) 
    
    

    user = relationship('User', back_populates='carts', foreign_keys=[user_id])
    supplement = relationship('Supplement', back_populates='cart_items', foreign_keys=[supplement_id])

    def __repr__(self):
        return  f"<Cart(user_name={self.user_name}, supplement_name={self.supplement_name}, supplement_price={self.supplement_price}, quantity={self.quantity})>"
    
    @classmethod
    def create(cls, session, user_name, supplement_name, supplement_price, quantity, user_id, supplement_id):
        cart_item = cls(user_name=user_name,
            supplement_name=supplement_name,
            supplement_price=supplement_price,
            quantity=quantity,
            user_id=user_id,
            supplement_id=supplement_id)
        session.add(cart_item)
        session.commit()
        return cart_item

    @classmethod
    def delete(cls, session, cart_id):
        cart_item = session.query(cls).get(cart_id)
        if cart_item:
            session.delete(cart_item)
            session.commit()
        else:
            raise ValueError("Cart item not found.")

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, cart_id):
        return session.query(cls).get(cart_id)