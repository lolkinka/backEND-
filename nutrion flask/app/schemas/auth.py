from marshmallow import Schema, fields, validate, ValidationError
from email_validator import validate_email, EmailNotValidError


def validate_email_format(email):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise ValidationError(str(e))


class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True, validate=validate_email_format)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate_email_format)
    password = fields.Str(required=True, validate=validate.Length(min=6))
