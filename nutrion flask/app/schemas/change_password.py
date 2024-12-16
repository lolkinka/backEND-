from marshmallow import Schema, fields, validate, ValidationError


def validate_new_password(password):
    if len(password) < 6:
        raise ValidationError("Новый пароль должен содержать не менее 6 символов.")


class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(required=True, validate=validate_new_password, load_only=True)
