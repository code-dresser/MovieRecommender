from flask import Blueprint,redirect,url_for,render_template
import wtforms


auth = Blueprint("auth",__name__,template_folder="templates/auth", url_prefix="/auth")


@auth.route("/login",methods=["GET","POST"])
def login_page():
    login_form = wtforms.Form()
    return render_template("login.html")

@auth.route("/signup",methods=["GET","POST"])
def signup_page():
    return render_template("signup.html")    
