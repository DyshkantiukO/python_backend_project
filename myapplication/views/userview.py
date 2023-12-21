from flask import request, jsonify
from marshmallow import ValidationError
from .. import app, db, schemas, models
from ..utils import add, delete
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256


@app.get('/users')
@jwt_required()
def get_users():
    users = [{"id": user.id, "name": user.name} for user in db.session.query(models.User).all()]
    return jsonify(users)


@app.get('/user')
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    try:
        user = db.session.query(models.User).filter(models.User.id == user_id).first()
        return jsonify({"id": user.id, "name": user.name})
    except AttributeError:
        return jsonify({"error": "AttributeError", "status_code": 404})


@app.post('/user')
def add_user():
    user_data = request.get_json()
    try:
        schemas.UserSchema().load({"name": user_data["name"], "password": user_data["password"]})
        existing_user = db.session.query(models.User).filter(models.User.name == user_data["name"]).first()
        if existing_user is not None:
            return jsonify({"error": "User already exists", "status_code": 404})
        user = models.User(user_data["name"], password=pbkdf2_sha256.hash(user_data["password"]))
        add(user)
        account_data = {"user_id": user.id, "money": user_data["money"]}
        schemas.AccountSchema().load(account_data)
        account = models.Account(user.id, user_data["money"])
        add(account)
        return jsonify({"id": user.id, "name": user.name, "money": account.money})
    except ValidationError as error:
        return error.messages


@app.post('/login')
def login_user():
    user_data = request.get_json()
    schemas.UserSchema().load({"name": user_data["name"], "password": user_data["password"]})
    name = user_data["name"]
    provided_user_id = user_data["id"]
    with app.app_context():
        user = models.User.query.filter_by(id=provided_user_id).first()
        if not user:
            return jsonify({"error": "Login unsuccessful - User not found", "status_code": 404})
        if provided_user_id is None or name != user.name:
            return jsonify({"error": "Login unsuccessful - invalid User ID or name", "status_code": 401})
        if not pbkdf2_sha256.verify(user_data["password"], user.password):
            return jsonify({"error": "Login unsuccessful - invalid password", "status_code": 401})
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": access_token, "user_id": user.id}), 200


@app.delete('/user')
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    deleted_user = delete(models.User, user_id)
    if deleted_user:
        return jsonify(deleted_user)
    else:
        return jsonify({"error": "AttributeError", "status_code": 404})
