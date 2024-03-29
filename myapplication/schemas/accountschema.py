from marshmallow import Schema, fields


class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    money = fields.Float(required=True)
