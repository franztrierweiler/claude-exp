"""Flask application entry point for Azure App Service."""
import os
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
