import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
# this is as our database for now
from db import stores

# Blueprint from flask_smorest is used to divide an API into multiple segments
blp = Blueprint("stores", __name__, description="Operations on stores")


# using MethodView, we can create a call where each method will route to specific endpoint
@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    @blp.response(200, StoreSchema)
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
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists")

        store_id = uuid.uuid4().hex
        print(store_id)
        # ** will unpack the values in store_data and all the "id" field we added in new_store object
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
