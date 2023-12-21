from flask import request, jsonify
from .. import app, db, models
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.get('/account')
@jwt_required()
def get_account():
    user_id = get_jwt_identity()
    try:
        account = db.session.query(models.Account).filter(models.Account.user_id == user_id).first()
        return jsonify({"user_id": account.user_id, "money": account.money})
    except AttributeError:
        return jsonify({"error": "AttributeError", "status_code": 404})
