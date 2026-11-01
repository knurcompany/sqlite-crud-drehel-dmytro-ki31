"""SQLite DAL: SQL is kept separate from Flask routes."""
import sqlite3
from contextlib import closing
from flask import current_app

SCHEMA='''CREATE TABLE IF NOT EXISTS tasks (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 120),
 description TEXT NOT NULL DEFAULT '',
 status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new','in_progress','done')),
 due_date TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)'''

def create_connection():
 connection=sqlite3.connect(current_app.config['DATABASE'])
 connection.row_factory=sqlite3.Row
 return connection

def create_db_table():
 with closing(create_connection()) as connection, connection:
  connection.execute(SCHEMA)

def insert_item(data):
 with closing(create_connection()) as connection, connection:
  cursor=connection.execute('INSERT INTO tasks(title,description,status,due_date) VALUES(?,?,?,?)',
   (data['title'],data['description'],data['status'],data['due_date']))
  return cursor.lastrowid

def get_all_items():
 with closing(create_connection()) as connection:
  return connection.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()

def get_item_by_id(item_id):
 with closing(create_connection()) as connection:
  return connection.execute('SELECT * FROM tasks WHERE id=?',(item_id,)).fetchone()

def update_item(item_id,data):
 with closing(create_connection()) as connection, connection:
  cursor=connection.execute('UPDATE tasks SET title=?,description=?,status=?,due_date=? WHERE id=?',
   (data['title'],data['description'],data['status'],data['due_date'],item_id))
  return cursor.rowcount==1

def delete_item(item_id):
 with closing(create_connection()) as connection, connection:
  return connection.execute('DELETE FROM tasks WHERE id=?',(item_id,)).rowcount==1
