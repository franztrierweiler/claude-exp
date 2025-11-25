"""Flask application initialization."""
from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app
