from marshmallow import Schema, fields, validate, ValidationError


def validate_positive(value):
    if value is not None and value < 0:
        raise ValidationError("Значение должно быть положительным.")


def validate_code_length(code):
    if len(code) != 13:
        raise ValidationError("Штрих-код должен содержать ровно 13 символов.")


class ProductCodeSchema(Schema):
    code = fields.Str(required=True, validate=validate_code_length)
    product_name = fields.Str(validate=validate.Length(min=1))
    score = fields.Str(validate=validate.Length(min=1))
    energy = fields.Float(validate=validate_positive, allow_none=True)
    fat = fields.Float(validate=validate_positive, allow_none=True)
    sugars = fields.Float(validate=validate_positive, allow_none=True)
    fiber = fields.Float(validate=validate_positive, allow_none=True)
    protein = fields.Float(validate=validate_positive, allow_none=True)
    salt = fields.Float(validate=validate_positive, allow_none=True)
