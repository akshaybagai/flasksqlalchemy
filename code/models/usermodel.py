import sqlite3
from ..db import db

from flask_restful import Resource, reqparse

class UserModel(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = UserModel(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(self, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where id = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = UserModel(*row)
        else:
            user = None

        connection.close()
        return user