import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import StoreList, Store

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # db_system / db_default
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

app.secret_key = '\xbd\xbaK\xfd\xdb\x133\x0c\xdfc\xbd\x90\x8a\x10\xe0V\x97\xf9\x8a\xa5;h\x88)'
jwt = JWT(app, authenticate, identity) # cria /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port = 5000, debug=True)
