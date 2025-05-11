# tests for database handler
import sqlite3
import pytest
from db import register_user, get_user_info, with_db_conn  # Import from the db package


# Fixture to set up the in-memory database
@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")  # Create an in-memory SQLite DB
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL
                   )
                   ''')
    conn.commit()

    # Return the connection and cursor for use in tests
    yield cursor, conn

    # Cleanup after test
    cursor.close()
    conn.close()


def test_register_user(db_connection):
    """
    Test the register_user function.
    """
    cursor, conn = db_connection

    # Use the original function, bypassing the decorator by calling __wrapped__
    original_register_user = register_user.__wrapped__  # Get the original function without the decorator
    original_register_user(cursor, 'john_doe', 'password123')

    cursor.execute("SELECT username, password FROM users WHERE username = 'john_doe'")
    user = cursor.fetchone()

    # Assert the user was registered successfully
    assert user[0] == 'john_doe'
    assert user[1] == 'password123'


def test_get_user_info(db_connection):
    """
    Test the get_user_info function.
    """
    cursor, conn = db_connection

    # Insert user data directly into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('john_doe', 'password123'))
    conn.commit()  # Commit changes to make sure the data is saved

    # Use the original function, bypassing the decorator by calling __wrapped__
    original_get_user_info = get_user_info.__wrapped__  # Get the original function without the decorator
    user = original_get_user_info(cursor, 'john_doe')

    # Assert the user data is correct
    assert user[0] == 'john_doe'
    assert user[1] == 'password123'
