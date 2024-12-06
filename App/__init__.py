import flask
from flask_login import current_user
from .blueprints.public.public import public
from .blueprints.auth.auth import auth
from .blueprints.user.user import user
from dotenv import load_dotenv
from .extentions import db,bcrypt,login_manager
from datetime import datetime, timezone
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
    login_manager.login_view='auth.login_page'
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    from .Models import User
    #user loading function
    @login_manager.user_loader
    def load_user(User_ID):
        return User.query.get(int(User_ID))
    # 404 handling
    @app.errorhandler(404)
    def not_found(e):
        return flask.render_template('404page.html'), 404
    
    # update value of user last_seen  
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now(timezone.utc)
            db.session.commit()
    # Set up the main route
    app.register_blueprint(public)
    app.register_blueprint(auth)
    app.register_blueprint(user)

    return app
