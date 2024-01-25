# set up app config
from flask import Flask
# import routes then register them
from app.routes import home, dashboard, api
# Note that you can import home directly from the routes package,
# because its __init__.py file imported (and renamed) the blueprint.
# Otherwise, you'd have to add from app.routes.home import bp as
# home and then repeat that line for any new modules that you added to routes.
from app.db import init_db
import logging
from app.utils import filters
# When Flask runs the app package, it tries to call a create_app() function.
# The app should serve any static resources from the root directory and not from the default /static directory.
# Trailing slashes are optional (/dashboard and /dashboard/ load the same route).
# The app should use the key called 'super_secret_key' when creating server-side sessions.
# The test_config=None parameter is often used in Flask applications to allow for overriding the default configuration


def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    # Enabling debug mode
    app.debug = True
    app.config.from_mapping(
        SECRET_KEY='super_secret_key'  # you can create sessions in Flask only if you've defined a secret key.
    )
    # register the filters with the app context
    app.jinja_env.filters['format_url'] = filters.format_url
    app.jinja_env.filters['format_date'] = filters.format_date
    app.jinja_env.filters['format_plural'] = filters.format_plural
    app.register_blueprint(api)   # add to register the blueprint
    # Now any routes that we define in the api.py module
    # will automatically become part of the Flask app and have a prefix of /api.
    if test_config:
        # Apply the test configuration if it's provided
        app.config.from_mapping(test_config)

    @app.route('/hello')    # route endpoint /hello
    def hello():
        return 'hello world'
    # register routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    # initialize the seeds
    init_db(app)  # pass app here, app contains the teardown method in its context, ending the db connection when done
    return app


#  steps:
#  1) Setup venv: '. venv/bin/activate'
#  2) Install Flask 'pip install flask' : use flask to render Jinja2 templates (similar to handlebars)
#  3) Setup sqlalchemy, pysql, dotenv : 'pip install sqlalchemy pymysql python-dotenv'
#  4) Setup db folder, __init__.py to establish db connection & Schema
#  5) Setup Models and import 'Base' from app.db folder (SQL models resemble classes in python)
#  6) Setup validation in models using the @validates decorator
#  7) Install bcrypt for password encryption: 'pip install bcrypt cryptography'
