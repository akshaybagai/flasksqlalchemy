from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask import Flask, jsonify, request, render_template
import sqlite3

# instead of a method at a time, you can have a resource and then bind urls with them
from code.models.itemmodel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message', "An item with name {} already exits".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': 'error in inserting item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()

        return {'message': 'item deleted'}

    # PUT method is always idempotent
    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = {'name': name, 'price': data['price']}
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemsList(Resource):
    def get(self):
        return {'item': items}
