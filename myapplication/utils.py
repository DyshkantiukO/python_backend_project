from myapplication import app, db
from flask_jwt_extended import JWTManager
from flask import jsonify


jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401


def add(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(model_class, item_id):
    try:
        item = db.session.query(model_class).filter(model_class.id == item_id).first()
        if item:
            deleted_item = {"id": item.id, **item.to_dict()}
            db.session.delete(item)
            db.session.commit()
            return deleted_item
        else:
            return None
    except AttributeError:
        return None
