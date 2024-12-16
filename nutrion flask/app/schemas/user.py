from marshmallow import Schema, fields
from .product import ProductSchema


class UserProductSchema(Schema):
    product = fields.Nested(ProductSchema)
    date_added = fields.DateTime()


class UserSavedProductsSchema(Schema):
    saved_products = fields.List(fields.Nested(UserProductSchema))
