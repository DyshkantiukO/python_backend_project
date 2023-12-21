from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True)