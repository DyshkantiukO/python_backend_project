from flask import request, jsonify
from marshmallow import ValidationError
from .. import app, db, schemas, models
from ..utils import add, delete


@app.get('/categories')
def get_categories():
    categories = [{"id": category.id, "name": category.name} for category in db.session.query(models.Category).all()]
    return jsonify(categories)


@app.get('/category')
def get_category():
    category_id = request.args.get('categoryID')
    try:
        schemas.CategorySchema().load({"id": category_id, "name": "instance"})
        category = db.session.query(models.Category).filter(models.Category.id == category_id).first()
        return jsonify({"id": category.id, "name": category.name})
    except (ValidationError, AttributeError):
        return "AttributeError, 404"


@app.post('/category')
def create_category():
    category_data = request.get_json()
    try:
        schemas.CategorySchema().load({"name": category_data["name"]})
        if db.session.query(models.Category).filter(models.Category.name == category_data["name"]).first() is None:
            category = models.Category(category_data["name"])
            add(category)
            return jsonify({"id": category.id, "name": category.name})
        else:
            return "CategoryExist, 404"
    except ValidationError as error:
        return error.messages


@app.delete('/category')
def delete_category():
    category_id = request.args.get('categoryID')
    deleted_category = delete(models.Category, category_id)
    if deleted_category:
        return jsonify(deleted_category)
    else:
        return "AttributeError, 404"
