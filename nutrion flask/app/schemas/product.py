from marshmallow import Schema, fields, validate, ValidationError


def validate_positive(value):
    if value is not None and value < 0:
        raise ValidationError("Значение должно быть положительным.")


class ProductDetailsSchema(Schema):
    product_name = fields.Str(required=True, validate=validate.Length(min=1))
    score = fields.Str(required=False, validate=validate.Length(min=1))
    energy = fields.Float(validate=validate_positive, allow_none=True)
    fat = fields.Float(validate=validate_positive, allow_none=True)
    sugars = fields.Float(validate=validate_positive, allow_none=True)
    fiber = fields.Float(validate=validate_positive, allow_none=True)
    protein = fields.Float(validate=validate_positive, allow_none=True)
    salt = fields.Float(validate=validate_positive, allow_none=True)


class ProductSchema(Schema):
    code = fields.Str(required=True, validate=validate.Length(equal=13))
    product = fields.Nested(ProductDetailsSchema, required=True)

