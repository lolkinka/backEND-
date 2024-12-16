from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, ma

from .routes.auth import auth_bp
from .routes.product import product_bp
from .routes.profile import profile_bp
from .routes.user import user_bp

import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')

    if not app.debug:
        handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=10)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    return app
