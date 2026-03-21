"""
Creates the database tables using the Postgres connection details in .env.
Run once before first use. 
"""

from dotenv import load_dotenv

from database.connection import get_engine
from database.schema import create_tables

if __name__ == "__main__":
    load_dotenv()
    engine = get_engine()
    create_tables(engine)