from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Cannot be blank!')
    parser.add_argument('store_id', type=int, required=True, help='Cannot be blank!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found!'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exists!'}

        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting an item!'}
        
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted!'}

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting an item!'}

        return item.json()

    
class ItemList(Resource):
    def get(self):
        return {'Items': [item.json() for item in ItemModel.query.all()]}