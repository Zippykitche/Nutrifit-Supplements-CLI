from db.models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Supplement(Base):
    __tablename__ = 'supplements'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    category = Column(String)

    cart_items = relationship('Cart', back_populates='supplement', foreign_keys='Cart.supplement_id')

    def __repr__(self):
        return f"<Supplement(name='{self.name}', description={self.description}, price={self.price}, quantity={self.quantity}, category={self.category})>"
    
    @property
    def is_in_stock(self):
        return self.quantity > 0

    # ORM Methods
    @classmethod
    def create(cls, session, name, description, price, quantity, category):
        supplement = cls(
            name=name, description=description, price=price, quantity=quantity, category=category
        )
        session.add(supplement)
        session.commit()
        return supplement

    @classmethod
    def delete(cls, session, supplement_id):
        supplement = session.query(cls).get(supplement_id)
        if supplement:
            session.delete(supplement)
            session.commit()
        else:
            raise ValueError("Supplement not found.")

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, supplement_id):
        return session.query(cls).get(supplement_id)
    
    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls.name == name).first()
    


