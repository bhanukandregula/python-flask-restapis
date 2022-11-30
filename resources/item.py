import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

# this is as our database for now
from db import items

# Blueprint from flask_smorest is used to divide an API into multiple segments
blp = Blueprint("items", __name__, description="Operations on items")


@blp.get("/item/<string:item_id>")
class Items(MethodView):

    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()
        if "item_price" not in item_data or "item_name" not in item_data:
            abort(400, message="Item not found")
        try:
            item = items[item_id]
            # this is a new update operator in python
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):

    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()

        # Check if the required values are present or not
        if "item_price" not in item_data or "store_id" not in item_data or "item_name" not in item_data:
            abort(400, message="Bad request, ensure to have price, store_id and name are included in the JSON payload")

        # check if the same item is already in the dictionary before adding as a new item
        for item in items.values():
            if item_data["item_name"] == item["item_name"] and item_data["store_id"] == item["store_id"]:
                abort(400, message="Item already exists")

        if item_data["store_id"] not in stores:
            # return {"message": "Store not found"}, 404
            # this abort is a functionality is from smorest package
            # we also don;t need to have return keyword here, abort will take care of sending response to client
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
