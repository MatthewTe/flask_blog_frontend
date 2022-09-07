import os
from flask import Flask

# Application Factory:
def create_app():

    app = Flask(__name__, instance_relative_config=False)
    
    # Registering configuration: 
    if os.environ.get("PRODUCTION", False):
        app.config.from_object('config.ProdConfig')
    else:
        app.config.from_object('config.DevConfig')

    with app.app_context():
        from .blog import blog_bp

        # Registering blueprints:
        app.register_blueprint(blog_bp, url_prefix="/blog")

        return app
