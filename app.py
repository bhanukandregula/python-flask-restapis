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
                "item_price": 79.99
            },
            {
                "item_name": "HP Desktop AMD Razen 12GB RAM",
                "item_price": 540.00
            }
        ]
    }
]


# This will fetch all the stores we have in dictionary defined above
@app.get("/stores")
def get_stores():
    # order of the key value might be different when it renders on the response
    # it shouldn't be always same
    return {"stores": stores}


# let's create a store and append to dictionary list
@app.post("/store")
def create_store():
    # 01. Get the JSON data which is sending by client
    request_data = request.get_json()
    # 02. Append the new store name to existing dictionary
    new_store = {"name": request_data["name"], "items" : []}
    stores.append(new_store)
    # 03. Return the success confirmation back to client
    return new_store, 201


if __name__ == '__main__':
    app.run()
