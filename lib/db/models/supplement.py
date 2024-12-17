from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

Base = declarative_base()

class Supplement(Base):
    __tablename__ = 'supplements'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    category = Column(String)

    def __repr__(self):
        return f"<Supplement(name='{self.name}', price={self.price}, quantity={self.quantity}, category={self.category})>"
    


