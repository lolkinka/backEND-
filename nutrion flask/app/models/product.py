from ..extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(13), unique=True, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.String(10), nullable=True)
    energy = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    sugars = db.Column(db.Float, nullable=True)
    fiber = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    salt = db.Column(db.Float, nullable=True)

    saved_by_users = db.relationship('UserProduct', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Product {self.code}>"
