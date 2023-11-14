from app.routes import home, dashboard, api # import the home, dashboard, api blueprint
from flask import Flask
from app.db import init_db
from app.utils import filters

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
    # register api blueprint here
    app.register_blueprint(api)

    # initialize database
    init_db(app)

    # register jinja filters
    app.jinja_env.filters['format_url'] = filters.format_url
    app.jinja_env.filters['format_date'] = filters.format_date
    app.jinja_env.filters['format_plural'] = filters.format_plural

    return app