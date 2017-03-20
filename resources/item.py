from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    # allows you to keep only certain parts of the request
    parser = reqparse.RequestParser()

    #looks in request payload and form payload
    parser.add_argument('price', # terminates if no price and returns help
                        type=float, #requires price to be float
                        required=True, # request cannot go through w/o price
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id', # terminates if no price and returns help
                        type=int, #requires price to be float
                        required=True, # request cannot go through w/o price
                        help="Every item needs a store id"
                        )

    @jwt_required() #means jwtoken has to be authenticated before get() can run
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
        except:
            return {'message': 'An error occured during query'}, 500 # internal server error

        return {'message': 'Item not found'}, 404

    # need the name parameter
    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) # **data instead of data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500 # internal server error

        return item.json(), 201 # status code 201 is for created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) # ** instead of data['price'], data['store_id']
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # list comprehension, preferred version
        return {'item': [item.json() for item in ItemModel.query.all()]}

        # lambda list, only us map if working with other programming languages
        # return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))}
