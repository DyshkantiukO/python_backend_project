from flask import request, jsonify
from .. import app, db, models


@app.get('/account')
def get_account():
    user_id = request.args.get('userID')
    try:
        account = db.session.query(models.Account).filter(models.Account.user_id == user_id).first()
        return jsonify({"user_id": account.user_id, "money": account.money})
    except AttributeError:
        return "AttributeError, 404"
