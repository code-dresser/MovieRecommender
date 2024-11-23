import flask
from blueprints.public.public import public
from blueprints.auth.auth import auth
from dotenv import load_dotenv
import os
app = flask.Flask(__name__, template_folder='templates')
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY") or "you-will-never-guess-it"
# Set up the main route
app.register_blueprint(public)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
