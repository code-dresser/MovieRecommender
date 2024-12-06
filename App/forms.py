from flask_wtf import FlaskForm
from wtforms import RadioField,TextAreaField,SubmitField,HiddenField,StringField
from wtforms.validators import InputRequired,DataRequired,Length

class ReviewForm(FlaskForm):

    movie_ID = HiddenField("movie_id",validators=[DataRequired()])
    title = StringField("title",validators=[DataRequired()])
    rating = RadioField("rating",choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5")])
    review_text = TextAreaField("Treść recenzji",validators=[DataRequired(),Length(min=1,max=250)])
    submit = SubmitField()
    

class UserForm(FlaskForm):
    first_name = StringField("first_name",validators=[DataRequired()])
    last_name = StringField("last_name",validators=[DataRequired()])
    email = StringField("email",validators=[DataRequired()])
    Bio = TextAreaField("first_name",validators=[Length(min=0,max=500)])
    submit = SubmitField()