from flask import Flask, jsonify, request, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from code.resources.user import UserRegister
from code.resources.item import Item, ItemsList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
    {
        "name": "item1",
        "price": 10
    }
]

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "item1",
                "price": 10
            }
        ]
    }
]


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

@app.route("/")
def home():
    return render_template("../templates/index.html")

@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    newstore = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(newstore)
    return jsonify(newstore)

@app.route('/store/<string:name>')
def get_store(name):
    for st in stores:
        if st["name"] == name:
            return jsonify(st)
    return jsonify({"message": 'store not found'})

@app.route('/store')
def get_stores():
    return jsonify(stores)


@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for st in stores:
        if st["name"] == name:
            new_item = {
                'name' : request_data['name'],
                'price': request_data['price']
            }
            st["items"].append(new_item)
            return jsonify(st)
    return jsonify({"message": 'store not found'})


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for st in stores:
        if st["name"] == name:
            return jsonify({"items": st['items']})
    return jsonify({"message": 'store not found'})


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
