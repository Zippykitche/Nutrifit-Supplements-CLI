from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import os


from db.models.supplement import Supplement
from db.models.user import User
from db.models.cart import Cart

fake = Faker()

db_path = os.path.join(os.path.dirname(__file__), 'nutrifit.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def seed_supplements(n=10):
    categories = ["Protein", "Vitamins", "Performance", "Energy", "Recovery"]
    supplements = []
    for _ in range(n):
        supplement = Supplement(
            name=fake.unique.word().capitalize() + " " + random.choice(["Boost", "Max", "Pro", "Flex", "Ultra"]),
            description=fake.sentence(nb_words=10),
            price=round(random.uniform(10.0, 100.0), 2),
            quantity=random.randint(10, 200),
            category=random.choice(categories)
        )
        supplements.append(supplement)
    session.add_all(supplements)
    print(f"Seeded {n} supplements.")

def seed_users(n=5):
    users = []
    for _ in range(n):
        user = User(
            name=fake.name(),
            email=fake.unique.email()
        )
        users.append(user)
    session.add_all(users)
    print(f"Seeded {n} users.")

def seed_cart_entries(n=15):
    users = session.query(User).all()
    supplements = session.query(Supplement).all()

    if not users or not supplements:
        print("Ensure that users and supplements are seeded before adding cart entries.")
        return

    cart_entries = []
    for _ in range(n):
        user = random.choice(users)
        supplement = random.choice(supplements)

        if not user or not supplement:
            continue

        entry = Cart(
            user_id=user.id,
            supplement_id=supplement.id,
            quantity=random.randint(1, 5)
        )
        cart_entries.append(entry)

    session.add_all(cart_entries)
    session.commit()  
    print(f"Seeded {n} cart entries.")


def main():
    session.query(Cart).delete()
    session.query(User).delete()
    session.query(Supplement).delete()
    session.commit()

    seed_supplements(10)
    seed_users(5)
    seed_cart_entries(15)

    session.commit()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    main()
    



