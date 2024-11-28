from flask_wtf import FlaskForm
from wtforms import IntegerField,RadioField,TextAreaField,SubmitField
from wtforms.validators import InputRequired,DataRequired


class ReviewForm(FlaskForm):

    movie_ID = IntegerField("movie_id",validators=[DataRequired()])
    rating = RadioField("rating",validators=[DataRequired()],choices=[(1,"1★"),(2,"2★"),(3,"3★"),(4,"4★"),(5,"5★")])
    review_text = TextAreaField("Treść recenzji",validators=[DataRequired()])
    submit = SubmitField()