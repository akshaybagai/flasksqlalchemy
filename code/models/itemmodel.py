import sqlite3
from ..db import db
from flask_restful import Resource, reqparse

class ItemModel(db.Model):

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self,name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # similar to rest template
        return cls.query.filter_by(name=name).first()

    # similar to hibernate if the object id exists, the object is updated
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()