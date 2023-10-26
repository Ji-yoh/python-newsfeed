from app.routes import home, dashboard # import the home & dashboard blueprint
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY='super_secret_key',
    )

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # register routes
    app.register_blueprint(home)
    # register dashboard blueprint here
    app.register_blueprint(dashboard)

    return app