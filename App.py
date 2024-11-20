import flask
from blueprints.public.public import public

app = flask.Flask(__name__, template_folder='templates')
# Set up the main route
app.register_blueprint(public)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
