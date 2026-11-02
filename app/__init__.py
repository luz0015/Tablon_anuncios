from flask import Flask
from config import Config
from app.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.usuarios.routes import usuarios_bp
    from app.blueprints.categorias.routes import categorias_bp
    from app.blueprints.anuncios.routes import anuncios_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(anuncios_bp, url_prefix='/')

    return app
