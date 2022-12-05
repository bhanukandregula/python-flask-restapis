import uuid
from flask import request

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ItemSchema, ItemUpdateSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel

# this is as our database for now
# from db import items, stores

# Blueprint from flask_smorest is used to divide an API into multiple segments
blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # this is the functionality from flask SQLAlchemy but it is not available on Vanilla SQLAlchemy
        # this will get item from database
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.item_name = item_data["item_name"]
            item.item_price = item_data["item_price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())}
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        # put the item in the database, hence save it to db
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return item
