from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,BooleanField
from wtforms.validators import InputRequired,Email,EqualTo,Length

class LoginForm(FlaskForm):
    email = EmailField("email",validators=[Email(),InputRequired(message="Email is required")])
    password = PasswordField("password",validators=[InputRequired(message="Password is required")])
    remember_me = BooleanField("Remember Me")
    
class SignupForm(FlaskForm):
    username = StringField("username",validators=[InputRequired(message="Username is required")])
    email = EmailField('email',validators=[Email(),InputRequired(message="Email is required")])
    password = PasswordField('password',validators=[InputRequired(message="Password is required"),Length(8,message=f"Minimal password length is %(min)d"),])
    password_conf = PasswordField("confirm password",validators=[InputRequired(message="Please confirm your password"),EqualTo('password', message='Passwords must match')])
    
    