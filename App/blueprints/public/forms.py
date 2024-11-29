from flask_wtf import FlaskForm
from wtforms import RadioField,TextAreaField,SubmitField,HiddenField
from wtforms.validators import InputRequired,DataRequired


class ReviewForm(FlaskForm):

    movie_ID = HiddenField("movie_id",id="movie_id",validators=[DataRequired()])
    rating = RadioField("rating",validators=[DataRequired()],choices=[(1,"1★"),(2,"2★"),(3,"3★"),(4,"4★"),(5,"5★")])
    review_text = TextAreaField("Treść recenzji",validators=[DataRequired()])
    submit = SubmitField()