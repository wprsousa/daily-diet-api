from .diary_routes import diary_bp
from .user_routes import user_bp


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(diary_bp)
