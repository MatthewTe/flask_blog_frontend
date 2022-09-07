from os import environ, path

class DevConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    PORT = environ.get('PORT', 5000)

class ProdConfig:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    PORT = environ.get('PORT', 5000)
