from db import db


# this class is inherited from db.Model
class ItemModel(db.Model):
    # defining a table, with name = items
    __tablename__ = "items"

    # defining the columns
    # this will also do auto increment
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), unique=True, nullable=False)
    item_price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    # 1 store have 5 items as an example
    # each store will have many items to see
    # this is an perfect example for one-to-many relationships

    # store_id isa foreign_key which maps to id from the items model, since we can have many items in each store
    # store_id = db.Column(db.Integer, unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    # create a store object that has the above relationship
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
