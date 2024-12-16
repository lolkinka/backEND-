from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.user import User
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from ..schemas.auth import RegisterSchema, LoginSchema
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

    if confirm_password != password:
        return jsonify({"msg": "Пароли не совпадают"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Пользователь с таким email уже существует"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Пользователь успешно создан"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Имя пользователя уже существует"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"msg": "Внутренняя ошибка сервера"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "Email не найден"}), 401

    if not user.check_password(password):
        return jsonify({"msg": "Неверный пароль"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(days=1)
    )
    return jsonify(access_token=access_token), 200
