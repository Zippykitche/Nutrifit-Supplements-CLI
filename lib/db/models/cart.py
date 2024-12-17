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

    user = relationship('User', back_populates='carts')
    supplement = relationship('Supplement')

    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, supplement_id={self.supplement_id}, quantity={self.quantity})"
    
    @classmethod
    def create(cls, session, user_id, supplement_id, quantity):
        cart_item = cls(user_id=user_id, supplement_id=supplement_id, quantity=quantity)
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