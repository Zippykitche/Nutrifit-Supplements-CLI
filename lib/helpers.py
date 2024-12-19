import os
from db.models import Base
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models.supplement import Supplement
from db.models.user import User
from db.models.cart import Cart

db_path = os.path.join(os.path.dirname(__file__), "db", 'nutrifit.db') 
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def seed_database(supplements=10, users=5, cart_entries=15):
    """Seed the database with test data."""
    fake = Faker()

    # Seed supplements
    categories = ["Protein", "Vitamins", "Performance", "Energy", "Recovery"]
    for _ in range(supplements):
        session.add(Supplement(
            name=fake.unique.word().capitalize() + " " + random.choice(["Boost", "Max", "Pro", "Flex", "Ultra"]),
            description=fake.sentence(nb_words=10),
            price=round(random.uniform(10.0, 100.0), 2),
            quantity=random.randint(10, 200),
            category=random.choice(categories)
        ))

    # Seed users
    for _ in range(users):
        session.add(User(
            name=fake.name(),
            email=fake.unique.email()
        ))

    # Commit the session before seeding cart entries
    session.commit()

    # Seed cart entries
    user_ids = [user.id for user in session.query(User).all()]
    supplement_ids = [sup.id for sup in session.query(Supplement).all()]
    for _ in range(cart_entries):
        session.add(Cart(
            user_id=random.choice(user_ids),
            supplement_id=random.choice(supplement_ids),
            quantity=random.randint(1, 5)
        ))

    # Commit the session after all seeding is done
    session.commit()
    return f"Seeded {supplements} supplements, {users} users, and {cart_entries} cart entries."
