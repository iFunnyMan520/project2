from marshmallow import Schema, fields


class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenSchema(Schema):
    token = fields.String(required=True)


class UpdateMeSchema(TokenSchema):
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class FollowSchema(TokenSchema):
    _id = fields.String(required=True)
