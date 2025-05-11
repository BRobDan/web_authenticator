# This is the database handler

import sqlite3
from functools import wraps


# decorator for database functions that will establish a connection with the database and handle errors
def with_db_conn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect('database.db') as conn: # This will create database.db if it doesn't exist
                cursor = conn.cursor() # create cursor
                # create table users if it doesn't exist already
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                    )
                    ''')
                result = func(cursor, *args, **kwargs)
                return result
        except sqlite3.DatabaseError as e:
            raise
    return wrapper

@with_db_conn
def get_user_info(cursor, username):
    cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

@with_db_conn
def register_user(cursor, username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

