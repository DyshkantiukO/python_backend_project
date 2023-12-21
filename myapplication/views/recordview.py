from flask import request, jsonify
from marshmallow import ValidationError
from .. import app, db, schemas, models
from ..utils import add, update, delete


@app.get('/record')
def manage_record():
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    try:
        schemas.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": 1.0})
        record = db.session.query(models.Record).filter(models.Record.user_id == user_id, models.Record.category_id ==
                                                        category_id).first()
        return jsonify({"id": record.id, "user_id": record.user_id, "category_id": record.category_id, "time": record.
                       time, "amount_of_expenditure": record.amount_of_expenditure})
    except (ValidationError, AttributeError):
        return jsonify({"error": "AttributeError", "status_code": 404})


@app.post('/record')
def create_record():
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    amount_of_expenditure = request.args.get('amount')
    try:
        schemas.RecordSchema().load(
            {"user_id": user_id, "category_id": category_id, "amount_of_expenditure": amount_of_expenditure})
        user = db.session.get(models.User, user_id)
        category = db.session.get(models.Category, category_id)
        if user is None or category is None:
            return "User or category does not exist"
        account = db.session.query(models.Account).filter(models.Account.user_id == user_id).first()
        if account is None or account.money - float(amount_of_expenditure) <= 0:
            return "User account doesn't exist or insufficient funds"
        account.money -= float(amount_of_expenditure)
        update()
        record = models.Record(user_id, category_id, amount_of_expenditure)
        add(record)
        return jsonify(
            {"id": record.id, "user_id": record.user_id, "category_id": record.category_id, "time": record.time,
             "amount_of_expenditure": record.amount_of_expenditure})
    except ValidationError as error:
        return error.messages


@app.delete('/record')
def delete_record():
    record_id = request.args.get('recordID')
    if record_id.isdigit():
        deleted_record = delete(models.Record, record_id)
        if deleted_record:
            return jsonify(deleted_record)
        else:
            return jsonify({"error": "AttributeError", "status_code": 404})
    else:
        return "sqlalchemy.exc.DataError"
