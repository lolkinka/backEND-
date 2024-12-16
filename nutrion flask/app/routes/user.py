from flask import Blueprint, jsonify
from ..extensions import db
from ..models.user import User
from ..schemas.user import UserSavedProductsSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

user_saved_products_schema = UserSavedProductsSchema()


@user_bp.route('/products', methods=['GET'])
@jwt_required()
def get_saved_products():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Пользователь не найден"}), 404

    result = user_saved_products_schema.dump({"saved_products": user.saved_products})
    return jsonify(result), 200
