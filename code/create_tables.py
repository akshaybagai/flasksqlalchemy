import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

items_table = "create table if not exists items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(items_table)

connection.commit()

connection.close()
