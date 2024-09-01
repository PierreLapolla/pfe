from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key

    login_manager.init_app(app)

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
