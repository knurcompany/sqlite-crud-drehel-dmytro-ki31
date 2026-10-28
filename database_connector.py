"""Дрегель Дмитро, група КІ-31. Робота з таблицею книг."""
import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE = Path(__file__).with_name('data.db')
CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 2100),
    status TEXT NOT NULL
)'''


def create_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_db_table():
    with closing(create_connection()) as connection, connection:
        connection.execute(CREATE_TABLE_SQL)


def insert_item(data):
    with closing(create_connection()) as connection, connection:
        cursor = connection.execute(
            'INSERT INTO books(title, author, year, status) VALUES (?, ?, ?, ?)', data)
        return cursor.lastrowid


def get_all_items():
    with closing(create_connection()) as connection:
        return connection.execute('SELECT * FROM books ORDER BY id').fetchall()


def get_item_by_id(item_id):
    with closing(create_connection()) as connection:
        return connection.execute('SELECT * FROM books WHERE id = ?', (item_id,)).fetchone()


def update_item(item_id, new_data):
    with closing(create_connection()) as connection, connection:
        return connection.execute(
            'UPDATE books SET title = ?, author = ?, year = ?, status = ? WHERE id = ?',
            (*new_data, item_id)).rowcount


def delete_item(item_id):
    with closing(create_connection()) as connection, connection:
        return connection.execute('DELETE FROM books WHERE id = ?', (item_id,)).rowcount
