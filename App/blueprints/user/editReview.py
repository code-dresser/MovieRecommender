from flask_wtf import FlaskForm
from wtforms import RadioField,TextAreaField,SubmitField,HiddenField,StringField
from wtforms.validators import InputRequired,DataRequired,Length

class EditReviewForm(FlaskForm):

    review_id = HiddenField("review_id",id="review_id",validators=[DataRequired()])
    title = StringField("title",id="edit_review_title",validators=[DataRequired()])
    rating = RadioField("rating",id="edit_review_rating",choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5")])
    review_text = TextAreaField("review_text",id="edit_review_text",validators=[DataRequired(),Length(min=1,max=250)])
    submit = SubmitField()