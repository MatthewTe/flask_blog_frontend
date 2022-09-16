from os import environ, path

class DevConfig:
    FLASK_ENV = 'development'
    SECRET_KEY = "TEST SECRET KEY"
    DEBUG = True
    TESTING = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    PORT = environ.get('PORT', 5000)
    API_URL = environ.get("API_URL", "http://localhost:8000")

class ProdConfig:
    FLASK_ENV = 'production'
    SECRET_KEY = environ.get("SECRET_KEY", None)
    DEBUG = False
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    PORT = environ.get('PORT', 5000)
    API_URL = environ.get("API_URL", "http://rest-api:80")

