import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel
from schemas import StoreSchema

# this is as our database for now
# from db import stores

# Blueprint from flask_smorest is used to divide an API into multiple segments
blp = Blueprint("stores", __name__, description="Operations on stores")


# using MethodView, we can create a call where each method will route to specific endpoint
@blp.route("/store/<int:store_id>")
class Stores(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges Required to delete Store.")
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        # put the item in the database, hence save it to db
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with the name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")

        return store
