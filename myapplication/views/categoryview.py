from flask import request, jsonify
from marshmallow import ValidationError
from .. import app, db, schemas, models
from ..utils import add, delete
from flask_jwt_extended import jwt_required


@app.get('/categories')
@jwt_required()
def get_categories():
    categories = [{"id": category.id, "name": category.name} for category in db.session.query(models.Category).all()]
    return jsonify(categories)


@app.get('/category')
@jwt_required()
def get_category():
    category_id = request.args.get('categoryID')
    try:
        schemas.CategorySchema().load({"id": category_id, "name": "instance"})
        category = db.session.query(models.Category).filter(models.Category.id == category_id).first()
        return jsonify({"id": category.id, "name": category.name})
    except (ValidationError, AttributeError):
        return jsonify({"error": "AttributeError", "status_code": 404})


@app.post('/category')
@jwt_required()
def add_category():
    category_data = request.get_json()
    try:
        schemas.CategorySchema().load({"name": category_data["name"]})
        existing_category = db.session.query(models.Category).filter(
            models.Category.name == category_data["name"]).first()
        if existing_category is not None:
            return jsonify({"error": "Category already exists", "status_code": 404})
        category = models.Category(category_data["name"])
        add(category)
        return jsonify({"id": category.id, "name": category.name})
    except ValidationError as error:
        return error.messages


@app.delete('/category')
@jwt_required()
def delete_category():
    category_id = request.args.get('categoryID')
    deleted_category = delete(models.Category, category_id)
    if deleted_category:
        return jsonify(deleted_category)
    else:
        return jsonify({"error": "AttributeError", "status_code": 404})
