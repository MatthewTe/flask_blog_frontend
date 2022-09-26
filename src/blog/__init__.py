import os
from flask import Flask

from datetime import timedelta

# Application Factory:
def create_app():

    app = Flask(__name__, instance_relative_config=False)
    
    # Registering configuration: 
    if os.environ.get("PRODUCTION", False):
        app.config.from_object('config.ProdConfig')
    else:
        app.config.from_object('config.DevConfig')
    #app.config.from_object("config.DevConfig")
    # Configuring session object:
    app.permanent_session_lifetime = timedelta(days=5)

    #app.config.from_object('config.DevConfig')
    with app.app_context():

        
        from .auth.auth_routes import auth_bp # Authentication Routes:
        from .blog import blog_bp # Main Blog Routes

        # Registering blueprints:
        app.register_blueprint(auth_bp)
        app.register_blueprint(blog_bp)

        return app
