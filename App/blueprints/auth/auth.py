from flask import Blueprint,redirect,url_for,render_template,flash
from flask_login import login_user,login_required,logout_user
from .forms import LoginForm,SignupForm
from ...Models import User
from ...extentions import bcrypt,db


auth = Blueprint("auth",__name__,template_folder="templates/auth", url_prefix="/auth")

@auth.route("/login",methods=["GET","POST"])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email= login_form.email.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data
        user = User.query.filter_by(Email=email).first()
        if not user or not bcrypt.check_password_hash(user.Password_hash,password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login_page'))
        else:
            login_user(user,remember=remember_me)
            print(email,password,remember_me)
            return redirect(url_for("public.profile"))
    else:
        for error in login_form.errors.items():
            flash(f"{" ".join(error[1])}")
    return render_template("login.html",form=login_form)

@auth.route("/signup",methods=["GET","POST"])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email= form.email.data
        password = form.password.data
        if User.query.filter_by(Email=email).first():
            flash("User with this username already exist , you may want to login.")
            return redirect(url_for('auth.signup_page'))
        else:
            user = User(Username=username,Email=email,Password=password,Password_hash=bcrypt.generate_password_hash(password,12))
            db.session.add(user)
            db.session.commit()
            flash("User added sucessfully")
            return redirect(url_for("auth.login_page"))
    else:
        for error in form.errors.items():
            flash(f"{" ".join(error[1])}")
    return render_template("signup.html",form=form)    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.main'))
