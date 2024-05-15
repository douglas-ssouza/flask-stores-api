from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema, StoreUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/stores")
class StoreList(MethodView):
  @blp.response(200, StoreSchema(many=True))
  def get(self):
    return StoreModel.query.all()
  

  @blp.arguments(StoreSchema)
  @blp.response(201, StoreSchema)
  def post(self, store_data):
    store = StoreModel(**store_data)
    try:
      db.session.add(store)
      db.session.commit()
    except IntegrityError:
      abort(400, message="A store with that name already exists.")
    except SQLAlchemyError:
      abort(500, message="An error occurred while creating the store.")
    return store


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
  @blp.response(200, StoreSchema)
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store


  @blp.arguments(StoreUpdateSchema)
  @blp.response(200, StoreSchema)
  def put(self, store_data, store_id):
    store = StoreModel.query.get(store_id)
    if store:
      store.name = store_data["name"]
    else:
      store = StoreModel(id=store_id, **store_data)

    db.session.add(store)
    db.session.commit()

    return store


  def delete(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return { "message": "Store deleted." }, 200
