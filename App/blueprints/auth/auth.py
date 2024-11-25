from flask import Blueprint,redirect,url_for,render_template,flash
from .forms import LoginForm,SignupForm
from ...Models import User

auth = Blueprint("auth",__name__,template_folder="templates/auth", url_prefix="/auth")

@auth.route("/login",methods=["GET","POST"])
def login_page():
    
    users = User.query.order_by(User.Username).all()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email= login_form.email.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data
        print(email,password,remember_me)
    else:
        for error in login_form.errors.items():
            flash(f"{" ".join(error[1])}")
    return render_template("login.html",form=login_form,users=users)

@auth.route("/signup",methods=["GET","POST"])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email= form.email.data
        password = form.password.data
        password_conf = form.password_conf.data
    else:
        for error in form.errors.items():
            flash(f"{" ".join(error[1])}")
    return render_template("signup.html",form=form)    
