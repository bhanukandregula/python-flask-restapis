from flask import Flask

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
                "item_name": "Sony A7C Digital Mirorless Camera",
                "item_price": 1800.00
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



if __name__ == '__main__':
    app.run()
