import sqlite3
from flask_restful import Resource, reqparse

class ItemModel:

    def __init__(self,name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from items where name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            print(row)
            item = ItemModel(*row)
        else:
            item = None

        connection.close()
        return item