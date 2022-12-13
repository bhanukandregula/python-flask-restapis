# import uuid
import os
import secrets

import models

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db
# since we have _init__.py in models directory, we don;t need to import each model independently
# just importing models will have all the files inside the folder will get imported
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint


# request
# from db import stores, items
# from flask_smorest import abort

def create_app(db_url=None):
    app = Flask(__name__)
    # We need to register these blueprint with the APIs
    # Bit of configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"

    # this is for the API documentation
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    # this will generate long and random secret key
    #  secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "66288125300068410897556231054177692476"
    jwt = JWTManager(app)

    # when we receive jwt, this function runs
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401
        )

    # this is a function that run everytime we create a access_token, and let us extra info to jwt
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # In general, we need to look in the database and see weather the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token is expired", "error": "token_expired"}), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token", "error": "authorization_required"}), 401
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)

    return app

#
#
# # This will fetch all the stores and items we have in dictionary defined above
# @app.get("/stores")
# def get_stores():
#     return {"stores": list(stores.values())}
#
#
# # List only the store details and items purchased
# @app.get("/store/<string:store_id>")
# def get_store_info(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         # return {"message": "Store not found"}, 404
#         # this abort is a functionality is from smorest package
#         # we also don;t need to have return keyword here, abort will take care of sending response to client
#         abort(404, message="Store not found")
#
#
# @app.get("/item")
# def get_all_items():
#     # return "testing docker!!!"
#     return {"items": list(items.values())}
#
#
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         # return {"message": "Item not found"}, 404
#         # this abort is a functionality is from smorest package
#         # we also don;t need to have return keyword here, abort will take care of sending response to client
#         abort(404, message="Item not found")
#
#
# # update an existing item while passing item_id
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "item_price" not in item_data or "item_name" not in item_data:
#         abort(400, message="Item not found")
#     try:
#         item = items[item_id]
#         # this is a new update operator in python
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404, message="Item not found")
#
#
# @app.post("/store")
# def create_store():
#     store_data = request.get_json()
#
#     # check If name exists is in the JSON payload
#     if "name" not in store_data:
#         abort(400, message="Bad request, Endure 'name' is included in the JSON payload.")
#
#     # Check if the store already exists, before we're adding as a new store
#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             abort(400, message="Store already exists")
#
#     store_id = uuid.uuid4().hex
#     print(store_id)
#     # ** will unpack the values in store_data and all the "id" field we added in new_store object
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store
#     return store, 201
#
#
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#
#     # Check if the required values are present or not
#     if "item_price" not in item_data or "store_id" not in item_data or "item_name" not in item_data:
#         abort(400, message="Bad request, ensure to have price, store_id and name are included in the JSON payload")
#
#     # check if the same item is already in the dictionary before adding as a new item
#     for item in items.values():
#         if item_data["item_name"] == item["item_name"] and item_data["store_id"] == item["store_id"]:
#             abort(400, message="Item already exists")
#
#     if item_data["store_id"] not in stores:
#         # return {"message": "Store not found"}, 404
#         # this abort is a functionality is from smorest package
#         # we also don;t need to have return keyword here, abort will take care of sending response to client
#         abort(404, message="Store not found")
#
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#
#     return item, 201
#
#
# # delete store with store_id
# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted"}
#     except KeyError:
#         abort(400, message="Store deleted")
#
#
# # delete an item while passing item id
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted"}
#     except KeyError:
#         abort(404, message="Item not found")
#
#
# if __name__ == '__main__':
#     app.run()
