import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models.supplement import Supplement
from lib.db.models.user import User
from lib.db.models.cart import Cart


engine = create_engine('sqlite:///nutrifit.db')
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """NutriFit CLI: Manage supplements, users, and carts."""
    pass

# Command to view all supplements
@cli.command()
def view_supplements():
    """View all supplements."""
    supplements = session.query(Supplement).all()
    if supplements:
        click.echo("\n=== Supplements ===")
        for sup in supplements:
            click.echo(f"{sup.id}. {sup.name} - ${sup.price} ({sup.quantity} in stock, Category: {sup.category})")
    else:
        click.echo("No supplements found.")

# Command to add a supplement
@cli.command()
@click.option('--name', prompt="Supplement name", help="Name of the supplement.")
@click.option('--description', prompt="Description", help="Short description of the supplement.")
@click.option('--price', type=float, prompt="Price", help="Price of the supplement.")
@click.option('--quantity', type=int, prompt="Quantity", default=0, help="Quantity in stock.")
@click.option('--category', prompt="Category", help="Category of the supplement.")
def add_supplement(name, description, price, quantity, category):
    """Add a new supplement."""
    supplement = Supplement(name=name, description=description, price=price, quantity=quantity, category=category)
    session.add(supplement)
    session.commit()
    click.echo(f"Supplement '{name}' added successfully!")

# Command to delete a supplement
@cli.command()
@click.argument('supplement_id', type=int)
def delete_supplement(supplement_id):
    """Delete a supplement by ID."""
    supplement = session.query(Supplement).get(supplement_id)
    if supplement:
        session.delete(supplement)
        session.commit()
        click.echo(f"Supplement ID {supplement_id} deleted.")
    else:
        click.echo("Supplement not found.")

# Command to seed database
@cli.command()
@click.option('--supplements', default=10, help="Number of supplements to seed.")
@click.option('--users', default=5, help="Number of users to seed.")
@click.option('--cart_entries', default=15, help="Number of cart entries to seed.")
def seed_database(supplements, users, cart_entries):
    """Seed the database with test data."""
    from faker import Faker
    import random
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

    # Seed cart entries
    session.commit()
    user_ids = [user.id for user in session.query(User).all()]
    supplement_ids = [sup.id for sup in session.query(Supplement).all()]
    for _ in range(cart_entries):
        session.add(Cart(
            user_id=random.choice(user_ids),
            supplement_id=random.choice(supplement_ids),
            quantity=random.randint(1, 5)
        ))

    session.commit()
    click.echo(f"Seeded {supplements} supplements, {users} users, and {cart_entries} cart entries.")

# Command to view cart entries
@cli.command()
def view_cart():
    """View all cart entries."""
    carts = session.query(Cart).all()
    if carts:
        click.echo("\n=== Cart Entries ===")
        for cart in carts:
            click.echo(f"User ID: {cart.user_id}, Supplement ID: {cart.supplement_id}, Quantity: {cart.quantity}")
    else:
        click.echo("No cart entries found.")

# ---- New Menus ----

@cli.command()
def main_menu():
    """Main Menu."""
    while True:
        click.echo("\n--- Main Menu ---")
        click.echo("1. Manage Users")
        click.echo("2. Manage Supplements")
        click.echo("3. Manage Cart")
        click.echo("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            user_menu()
        elif choice == "2":
            supplement_menu()
        elif choice == "3":
            cart_menu()
        elif choice == "4":
            click.echo("Exiting NutriFit CLI. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")

def user_menu():
    """User Management Menu."""
    while True:
        click.echo("\n--- User Menu ---")
        click.echo("1. View All Users")
        click.echo("2. Add User")
        click.echo("3. Delete User")
        click.echo("4. Return to Main Menu")
        choice = input("Enter your choice: ").strip()
        

def supplement_menu():
    """Supplement Management Menu."""
    while True:
        click.echo("\n--- Supplement Menu ---")
        click.echo("1. View All Supplements")
        click.echo("2. Add Supplement")
        click.echo("3. Delete Supplement")
        click.echo("4. Return to Main Menu")
        choice = input("Enter your choice: ").strip()
       

def cart_menu():
    """Cart Management Menu."""
    while True:
        click.echo("\n--- Cart Menu ---")
        click.echo("1. View All Cart Entries")
        click.echo("2. Return to Main Menu")
        choice = input("Enter your choice: ").strip()
       

if __name__ == "__main__":
    cli()
