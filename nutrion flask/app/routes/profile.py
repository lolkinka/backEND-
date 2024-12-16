from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.user import User
from ..schemas.profile import UserProfileSchema
from ..schemas.change_password import ChangePasswordSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)

user_profile_schema = UserProfileSchema()
change_password_schema = ChangePasswordSchema()


@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Пользователь не найден"}), 404

    result = user_profile_schema.dump(user)
    return jsonify(result), 200


@profile_bp.route('/profile/password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Пользователь не найден"}), 404

    try:
        data = change_password_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    old_password = data['old_password']
    new_password = data['new_password']

    if not user.check_password(old_password):
        return jsonify({"msg": "Текущий пароль неверен"}), 401

    user.set_password(new_password)

    try:
        db.session.commit()
        return jsonify({"msg": "Пароль успешно изменен"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Внутренняя ошибка сервера"}), 500


@profile_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Пользователь не найден"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "Аккаунт успешно удален"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Внутренняя ошибка сервера"}), 500