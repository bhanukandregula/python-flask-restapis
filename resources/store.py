import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

# this is as our database for now
from db import stores

# Blueprint from flask_smorest is used to divide an API into multiple segments
blp = Blueprint("stores", __name__, description="Operations on stores")


# using MethodView, we can create a call where each method will route to specific endpoint
@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(400, message="Store deleted")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()

        # check If name exists is in the JSON payload
        if "name" not in store_data:
            abort(400, message="Bad request, Endure 'name' is included in the JSON payload.")

        # Check if the store already exists, before we're adding as a new store
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists")

        store_id = uuid.uuid4().hex
        print(store_id)
        # ** will unpack the values in store_data and all the "id" field we added in new_store object
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
