import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT name, price FROM items"

        items = []
        for row in cursor.execute(query):
            items.append(cls(*row))

        connection.commit()
        connection.close()

        return items
