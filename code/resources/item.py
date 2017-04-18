from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return { 'message': 'Item not found', 'status_code': 404 }, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message': "An item with name {} already exists".format(name), 'status_code': 400 }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save()
        except:
            return { 'error': 'An error occurred inserting an item', 'status_code': 500 }, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete()
            return { 'message': 'Item deleted', 'status_code': 204 }, 204

        return { 'message': 'Item not found', 'status_code': 404 }, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save()

        return item.json()

class ItemList(Resource):

    def get(self):
        # return { 'items': list(map(lambda item: item.json(), ItemModel.query.all())) }
        return { 'items': [item.json() for item in ItemModel.query.all()] } # parece mais claro
