from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    # this id will always map with the store_id from item model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")