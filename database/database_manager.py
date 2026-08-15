import sqlite3
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database Location
DATABASE_PATH = BASE_DIR / "database" / "enterprise_soc.db"


def get_connection():
    """
    Returns SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def execute_query(query, parameters=()):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query, parameters)

    connection.commit()

    connection.close()


def fetch_all(query, parameters=()):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    connection.close()

    return rows


def fetch_one(query, parameters=()):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query, parameters)

    row = cursor.fetchone()

    connection.close()

    return row