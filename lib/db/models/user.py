from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    carts = relationship('Cart', back_populates='user')

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
    
    @classmethod
    def create(cls, session, name, email):
        user = cls(name=name, email=email)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, user_id):
        user = session.query(cls).get(user_id)
        if user:
            session.delete(user)
            session.commit()
        else:
            raise ValueError("User not found.")

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, user_id):
        return session.query(cls).get(user_id)
    
    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls.name == name).first()
    