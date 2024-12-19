
NutriFit-Supplements-CLI

The NutriFit-Supplements-CLI is a command-line application designed to manage a supplement store. The app allows users to perform various operations, such as adding and viewing users, adding and removing items from a cart, viewing cart details, managing supplements, and seeding the database with test data.

Features

Manage supplements, users, and cart entries using a database powered by SQLAlchemy ORM.
Apply Python logic to database table columns and relationships.
Use Alembic for database migrations to maintain schema integrity.
Interactive CLI with detailed prompts and input validation.
Pre-seed the database with sample data using the Faker library.
Commands are implemented using Click, enabling structured, user-friendly command-line interfaces with options, arguments, and prompts.
**CLI Commands**:
  - Add supplements to the database.
  - View all supplements, users, and cart entries.
  - Add, update, and delete items in the user's cart.
**User Input Validation**:
  - Prompts user for input with validation checks.
  - Ensures correct data types and proper error handling.

Setup Instructions

1. Clone the Repository
git clone (https://github.com/Zippykitche/Nutrifit-Supplements-CLI)
cd NutriFit-Supplements-CLI
2. Install Dependencies
Ensure you have Python 3.8+ installed. Then, use pipenv to install dependencies:
run
pipenv install

This will install the following dependencies:

SQLAlchemy: ORM to interact with the database.
Alembic: Database migration tool.
Click: Command-line interface package.
Faker: Used for generating fake data for seeding the database.
ipdb: Debugging tool.

run
pipenv shell

3. Set Up the Database
cd into the lib/db directory, then run alembic init migrations to set up Alembic.
Modify line 58 in alembic.ini to point to the database you intend to create, then replace line 21 in migrations/env.py with the following:

from models import Base
target_metadata = Base.metadata

Navigate to models.py and start creating those models. Remember to regularly run alembic revision --autogenerate -m'<descriptive message>' and alembic upgrade head to track your modifications to the database and create checkpoints

4. Seed the Database
run python seed.py to seed database using faker()

run python cli.py or include the shebang and make it executable with chmod +x.
you can use the following CLI commands
cart-menu
supplement-menu
user-menu
e.g running python cli.py cart-menu will output:
--- Cart Menu ---
1. View All Cart Entries
2. Add Item to Cart
3. Delete Item from Cart
4. Return to Main Menu
Enter your choice: 1

--- Cart Entries ---
User: Dale Haynes, Supplement: Yard Pro, Quantity: 1, Price: 45.01

--- Cart Menu ---
1. View All Cart Entries
2. Add Item to Cart
3. Delete Item from Cart
4. Return to Main Menu
Enter your choice: 


Project Structure

Nutrifit-Supplements-CLI/
├── Pipfile
├── Pipfile.lock
├── README.md
├── lib/
│   ├── cli.py                  # Main CLI interface using click
│   ├── db/
│   │   ├── alembic.ini         # Alembic configuration file
│   │   ├── migrations/         # Folder for database migrations
│   │   │   ├── README          # Migration docs
│   │   │   ├── env.py          # Alembic environment script
│   │   │   ├── script.py.mako   # Mako template for migrations
│   │   │   └── versions/       # Folder for migration versions
│   │   ├── models/
│   │   │   ├── __init__.py     # Makes models a package
│   │   │   ├── cart.py         # Cart model
│   │   │   ├── supplement.py   # Supplement model
│   │   │   ├── user.py         # User model
│   │   ├── nutrifit.db         # SQLite database file
│   │   ├── seed.py             # Script to seed database with test data
│   ├── debug.py                # Debugging tools or helpers (if any)
├── lib/db/models/__init__.py   # Optional, if you want to treat models as a module 

