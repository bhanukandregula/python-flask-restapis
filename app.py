from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "Ikea",
        "items": [
            {
                "item_name": "Vegetables Filter",
                "item_price": 05.89
            },
            {
                "item_name": "Ice pops",
                "item_price": 06.99
            }
        ]
    },
    {
        "name": "Best Buy",
        "items": [
            {
                "item_name": "Bose Mini Speaker",
                "item_price": 79.990
            },
            {
                "item_name": "HP Desktop AMD Razen 12GB RAM",
                "item_price": 540.00
            }
        ]
    }
]


# This will fetch all the stores and items we have in dictionary defined above
@app.get("/stores")
def get_stores():
    # order of the key value might be different when it renders on the response
    # it shouldn't be always same
    return {"stores": stores}


# This will fetch the store names from all those store details in dictionary

@app.get("/get-store-names")
def get_only_store_names():
    temp = []
    temp.clear()
    for store in stores:
        temp.append(store["name"])
    return temp


# List only the store details and items purchased
@app.get("/store/<string:name>")
def get_store_info(name):
    for store in stores:
        if store["name"] == name:
            return store, 201
    return {"message": "Store not found"}, 404


# list all thr products only which are purchased in specific store
@app.get("/store/<string:name>/item")
def get_store_items_info(name):
    for store in stores:
        if store["name"] == name:
            return {"Items": store["items"]}
    return {"message": "Store not found to get items purchased"}, 404


# let's create a store and append to dictionary list
@app.post("/store")
def create_store():
    # 01. Get the JSON data which is sending by client
    request_data = request.get_json()
    # 02. Append the new store name to existing dictionary
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    # 03. Return the success confirmation back to client
    return new_store, 201


# Create an item for specific stores we have
@app.post("/store/<string:name>/item")
def create_item(name):
    # 01. get the data coming from client
    request_data = request.get_json()
    print("Request Data is :: > ", request_data)
    # 02. Check If we have store name send by client in our dictionary
    for store in stores:
        if store["name"] == name:
            new_item = {"item_name": request_data["item_name"], "item_price": request_data["item_price"]}
            store["items"].append(new_item)
            # 03. Return new item back to client after successful append to dictionary
            return new_item, 201
    return {"message": "Store not found"}, 404


if __name__ == '__main__':
    app.run()
