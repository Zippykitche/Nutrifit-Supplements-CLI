import os
import click
from db.models import Base 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from db.models.supplement import Supplement
from db.models.user import User
from db.models.cart import Cart


db_path = os.path.join(os.path.dirname(__file__), "db", 'nutrifit.db') 
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """NutriFit CLI: Manage supplements, users, and carts."""
    pass

# Command to view all supplements

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

def delete_supplement(supplement_input):
    """Delete a supplement by id or name."""
    if supplement_input.isdigit():
        supplement_id = int(supplement_input)
        supplement = session.query(Supplement).get(supplement_id)
        if supplement:
            session.delete(supplement)
            session.commit()
            click.echo(f"Supplement with ID {supplement_id} has been deleted.")
        else:
            click.echo(f"No supplement found with ID {supplement_id}.")
    else:
        supplement_name = supplement_input.strip()
        supplement = session.query(Supplement).filter(Supplement.name == supplement_name).first()
        if supplement:
            session.delete(supplement)
            session.commit()
            click.echo(f"Supplement '{supplement_name}' has been deleted.")
        else:
            click.echo(f"No supplement found with name '{supplement_name}'.")


# Command to view users

def view_users():
    """View all users."""
    users = session.query(User).all()
    if users:
        click.echo("\n=== Users ===")
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        click.echo("No users found.")

# Command to add users

@click.option('--name', prompt="User name", help="Name of the user.")
@click.option('--email', prompt="User email", help="Email of the user.")
def add_user(name, email):
    """Add a new user."""
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    click.echo(f"User '{name}' added successfully!")

# Command to delete users

def delete_user(user_input):
    """Delete a user by either user_id or username."""
    try:
        user_id = int(user_input)
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            click.echo(f"User with ID {user_id} has been deleted.")
        else:
            click.echo(f"No user found with ID {user_id}.")
    except ValueError:
        user = session.query(User).filter_by(name=user_input).first()
        if user:
            session.delete(user)
            session.commit()
            click.echo(f"User with username '{user_input}' has been deleted.")
        else:
            click.echo(f"No user found with username '{user_input}'.")

# Command to view all cart entries

from sqlalchemy.orm import joinedload

def view_cart():
    """View the contents of the cart."""
    cart_items = session.query(Cart).options(
        joinedload(Cart.user),      
        joinedload(Cart.supplement)  
    ).all()

    if not cart_items:
        click.echo("The cart is empty.")
    else:
        click.echo("\n--- Cart Entries ---")
        for item in cart_items:
            user = item.user
            supplement = item.supplement
            
            if user and supplement:
                click.echo(f"User: {user.name}, Supplement: {supplement.name}, Quantity: {item.quantity}, Price: {supplement.price}")
            else:
                click.echo(f"Item with ID {item.id} is incomplete.")



# Command to add an item to the cart
@click.option('--user_name', prompt="User Name", type=str, help="Name of the user.")
@click.option('--supplement_name', prompt="Supplement Name", type=str, help="Name of the supplement.")
@click.option('--quantity', prompt="Quantity", type=int, default=1, help="Quantity of the supplement to add to the cart.")
def add_to_cart(user_name, supplement_name, quantity):
    """Add a supplement to a user's cart by user identifier (ID or Name) and supplement identifier (ID or Name)."""
    
    if user_name.isdigit():  
        user = session.query(User).filter_by(id=int(user_name)).first()
    else: 
        user = session.query(User).filter_by(name=user_name).first()
    
    if not user:
        click.echo(f"User with name '{user_name}' not found.")
        return

    if supplement_name.isdigit():  
        supplement = session.query(Supplement).filter_by(id=int(supplement_name)).first()
    else:  
        supplement = session.query(Supplement).filter_by(name=supplement_name).first()

    if not supplement:
        click.echo(f"Supplement with name '{supplement_name}' not found.")
        return

    
    cart_item = Cart(user_name=user.name, supplement_name=supplement.name, supplement_price=supplement.price, quantity=quantity, user_id=user.id, supplement_id=supplement.id)
    session.add(cart_item)
    session.commit()
    
    click.echo(f"Added {quantity} of '{supplement.name}' (Price: {supplement.price} each) to {user.name}'s cart.")
    click.echo(f"User ID: {user.id}, Supplement ID: {supplement.id}")
    view_cart() 

# Command to delete cart item
def delete_from_cart():
    """Delete an item from the user's cart using supplement ID or name."""
    user_identifier = input("Enter User Identifier (ID or Name) to confirm: ").strip()

    # Confirm the user's identity
    if user_identifier.isdigit():
        user = session.query(User).filter_by(id=int(user_identifier)).first()
    else:
        user = session.query(User).filter_by(name=user_identifier).first()

    if not user:
        click.echo(f"No user found with identifier: {user_identifier}")
        return

    supplement_identifier = input("Enter Supplement Identifier (ID or Name) to remove: ").strip()

    # Find supplement by ID or Name
    if supplement_identifier.isdigit():  
        supplement = session.query(Supplement).filter_by(id=int(supplement_identifier)).first()
    else:  
        supplement = session.query(Supplement).filter_by(name=supplement_identifier).first()

    if not supplement:
        click.echo(f"No supplement found with identifier '{supplement_identifier}'")
        return

   
    cart_entries = session.query(Cart).filter_by(user_id=user.id, supplement_id=supplement.id).all()

    if not cart_entries:
        click.echo(f"No items found in cart for supplement '{supplement.name}' under user '{user.name}'.")
        return

    # Display the found cart entries
    click.echo(f"\nFound {len(cart_entries)} cart entry(ies) for supplement '{supplement.name}' by user '{user.name}':")
    for entry in cart_entries:
        click.echo(f"Cart Entry ID: {entry.id}, Quantity: {entry.quantity}")

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete these entries? (y/n): ").strip().lower()
    if confirm == 'y':
        for entry in cart_entries:
            session.delete(entry)
        session.commit()
        click.echo(f"Deleted {len(cart_entries)} cart entry(ies) for supplement '{supplement.name}' by user '{user.name}'.")
    else:
        click.echo("Deletion canceled.")

    view_cart()  


# ----  Menus ----

@cli.command()
def user_menu():
    """User Management Menu."""
    while True:
        click.echo("\n--- User Menu ---")
        click.echo("1. View All Users")
        click.echo("2. Add User")
        click.echo("3. Delete User")
        click.echo("4. Return to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_users()  
        elif choice == "2":
            name = input("Enter User Name: ").strip()
            email = input("Enter User Email: ").strip()
            add_user(name, email) 
        elif choice == "3":
            user_input = input("Enter User ID or Username to delete: ").strip()
            delete_user(user_input) 
        elif choice == "4":
            break
        else:
            click.echo("Invalid choice. Please try again.")
        
@cli.command()
def supplement_menu():
    """Supplement Management Menu."""
    while True:
        click.echo("\n--- Supplement Menu ---")
        click.echo("1. View All Supplements")
        click.echo("2. Add Supplement")
        click.echo("3. Delete Supplement")
        click.echo("4. Return to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_supplements()  
        elif choice == "2":
            name = input("Enter Supplement Name: ").strip()
            description = input("Enter Supplement Description: ").strip()
            price = input("Enter Supplement Price: ").strip()
            quantity = input("Enter Supplement Quantity: ").strip()
            category = input("Enter Supplement Category: ").strip()
           
            add_supplement(name, description, price, quantity, category) 
        elif choice == "3":
            supplement_input = input("Enter Supplement ID or Name to delete: ").strip()
            delete_supplement(supplement_input)
        elif choice == "4":
            break
        else:
            click.echo("Invalid choice. Please try again.")
       
@cli.command()
def cart_menu():
    """Cart Management Menu."""
    while True:
        click.echo("\n--- Cart Menu ---")
        click.echo("1. View All Cart Entries")
        click.echo("2. Add Item to Cart")
        click.echo("3. Delete Item from Cart")
        click.echo("4. Return to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_cart()

        elif choice == "2":
            user_identifier = input("Enter User Identifier (ID or Name): ").strip()
            if user_identifier.isdigit():  
                user = session.query(User).filter_by(id=int(user_identifier)).first()
            else:  
                user = session.query(User).filter_by(name=user_identifier).first()

            if not user:
                click.echo(f"No user found with identifier: {user_identifier}")
                continue

            supplement_identifier = input("Enter Supplement Identifier (ID or Name): ").strip()
            if supplement_identifier.isdigit():  
                supplement = session.query(Supplement).filter_by(id=int(supplement_identifier)).first()
            else: 
                supplement = session.query(Supplement).filter_by(name=supplement_identifier).first()

            if not supplement:
                click.echo(f"No supplement found with identifier: {supplement_identifier}")
                continue

            try:
                quantity = int(input("Enter Quantity: ").strip())
                add_to_cart(user_name=user.name, supplement_name=supplement.name, quantity=quantity)
                click.echo(f"Added {quantity} of {supplement.name} to {user.name}'s cart.")
            except ValueError:
                click.echo("Invalid input. Please enter a valid quantity.")

        elif choice == "3":
            user_identifier = input("Enter User Identifier (ID or Name) to confirm: ").strip()

            if user_identifier.isdigit():
                user = session.query(User).filter_by(id=int(user_identifier)).first()
            else:
                user = session.query(User).filter_by(name=user_identifier).first()

            if not user:
                click.echo(f"No user found with identifier: {user_identifier}")
                continue

            supplement_identifier = input("Enter Supplement Identifier (ID or Name) to remove: ").strip()

          
            if supplement_identifier.isdigit(): 
                supplement = session.query(Supplement).filter_by(id=int(supplement_identifier)).first()
            else:  
                supplement = session.query(Supplement).filter_by(name=supplement_identifier).first()

            if not supplement:
                click.echo(f"No supplement found with identifier '{supplement_identifier}'")
                continue

          
            cart_entries = session.query(Cart).filter_by(user_id=user.id, supplement_id=supplement.id).all()

            if not cart_entries:
                click.echo(f"No items found in cart for supplement '{supplement.name}' under user '{user.name}'.")
                continue

            
            click.echo(f"\nFound {len(cart_entries)} cart entry(ies) for supplement '{supplement.name}' by user '{user.name}':")
            for entry in cart_entries:
                click.echo(f"Cart Entry ID: {entry.id}, Quantity: {entry.quantity}")

           
            confirm = input(f"Are you sure you want to delete these entries? (y/n): ").strip().lower()
            if confirm == 'y':
                for entry in cart_entries:
                    session.delete(entry)
                session.commit()
                click.echo(f"Deleted {len(cart_entries)} cart entry(ies) for supplement '{supplement.name}' by user '{user.name}'.")
            else:
                click.echo("Deletion canceled.")

            view_cart()

        elif choice == "4":
            break

        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == "__main__":
    cli()
