from flask import Flask

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "item_name": "Chair",
                "item_price": 19.99
            }
        ]
    }
]


@app.get("/store")
def get_store():
    # order of the key value might be different when it renders on the response
    # it shouldn't be always same
    return {"stores": stores}


if __name__ == '__main__':
    app.run()
