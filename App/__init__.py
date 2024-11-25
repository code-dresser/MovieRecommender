import flask
from .blueprints.public.public import public
from .blueprints.auth.auth import auth
from dotenv import load_dotenv
from .extentions import db
import os

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = flask.Flask(__name__, template_folder='templates')
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY") or "you-will-never-guess-it"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['FLASK_ENV'] = 'development'
    app.config['DEBUG'] = True
    db.init_app(app)
    # Set up the main route
    app.register_blueprint(public)
    app.register_blueprint(auth)

    return app