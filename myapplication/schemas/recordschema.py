from marshmallow import Schema, fields


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    time = fields.Str(dump_only=True)
    amount_of_expenditure = fields.Float(required=True)
