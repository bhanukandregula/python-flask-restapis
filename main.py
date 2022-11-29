import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)


# This will fetch all the stores and items we have in dictionary defined above
@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


# List only the store details and items purchased
@app.get("/store/<string:store_id>")
def get_store_info(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    # ** will unpack the values in store_data and all the "id" field we added in new_store object
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    stores[item_id] = item

    return item, 201


if __name__ == '__main__':
    app.run()
