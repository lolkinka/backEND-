from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.product import Product
from ..schemas.product import ProductSchema
from ..schemas.product_code import ProductCodeSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user_product import UserProduct
from datetime import datetime

product_bp = Blueprint('product', __name__)

product_schema = ProductSchema()
product_code_schema = ProductCodeSchema()


@product_bp.route('/product', methods=['POST'])
@jwt_required()
def add_product():
    try:
        data = product_schema.load(request.get_json())
    except ValidationError as err:
        print(err)
        return jsonify({"errors": err.messages}), 400

    code = data['code']
    product_data = data['product']

    current_user_id = get_jwt_identity()

    product = Product.query.filter_by(code=code).first()

    if not product:
        product = Product(
            code=code,
            product_name=product_data.get('product_name'),
            score=product_data.get('score'),
            energy=product_data.get('energy'),
            fat=product_data.get('fat'),
            sugars=product_data.get('sugars'),
            fiber=product_data.get('fiber'),
            protein=product_data.get('protein'),
            salt=product_data.get('salt')
        )
        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Внутренняя ошибка сервера"}), 500

    user_product = UserProduct.query.filter_by(user_id=current_user_id, product_id=product.id).first()
    if user_product:
        return jsonify({"msg": "Продукт уже сохранен пользователем"}), 200

    user_product = UserProduct(
        user_id=current_user_id,
        product_id=product.id,
        date_added=datetime.now()
    )
    try:
        db.session.add(user_product)
        db.session.commit()
        return jsonify({"msg": "Продукт успешно добавлен и сохранен пользователем"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Внутренняя ошибка сервера"}), 500


@product_bp.route('/product/<code>', methods=['GET'])
def get_product(code):
    try:
        validated_data = product_code_schema.load({"code": code})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    code = validated_data['code']

    product = Product.query.filter_by(code=code).first()

    if not product:
        return jsonify({"msg": "Продукт не найден"}), 404

    result = product_code_schema.dump(product)
    return jsonify(result), 200
