from datetime import datetime
from ..extensions import db


class UserProduct(db.Model):
    __tablename__ = 'user_products'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='_user_product_uc'),)

    user = db.relationship('User', back_populates='saved_products')
    product = db.relationship('Product', back_populates='saved_by_users')

    def __repr__(self):
        return f"<UserProduct user_id={self.user_id} product_id={self.product_id}>"