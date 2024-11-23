import flask
from blueprints.public.public import public
from blueprints.auth.auth import auth

app = flask.Flask(__name__, template_folder='templates')
# Set up the main route
app.register_blueprint(public)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
