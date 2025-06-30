from flask import Flask
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

from database.database import db
from src.models.user import User
from src.routes import register_routes
from src.logger import logger

ma = Marshmallow()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
register_routes(app)

login_manager.login_view = "login"

logger.info("Aplicação Iniciando")


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, user_id)
    return user


if __name__ == "__main__":
    app.run(debug=True)
