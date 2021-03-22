from typing import List

from marshmallow import Schema, fields


class NewPostSchema(Schema):
    title: str = fields.String(required=True)
    tags: List[str] = fields.List(fields.String(), required=True)
    description: str = fields.String(required=True)
    only_for_followers: bool = fields.Boolean(required=True)


class IdSchema(Schema):
    _id: str = fields.String(required=True)


class PostsByTagSchema(Schema):
    tag: str = fields.String(required=True)
