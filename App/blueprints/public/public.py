from flask import Blueprint,redirect,render_template,url_for,request
from flask_login import login_required,current_user
from ...Models import Movie,Review
from  ... import Recomender
from ...extentions import db
from .forms import ReviewForm
recomender = Recomender.MovieRecomender(r"App\top25000_tmdb.csv",False)
recomender.select_features(['title','tagline','genres','cast','director','writers','producers'])
recomender.vectorise()
public = Blueprint("public", __name__,template_folder="templates/public")

@public.route('/', methods=['GET'])
def main():
    # Number of items per sublist 
    n = 3 
    movies = recomender.get_popular_movies()
    # Create sublists using list comprehension 
    sublists = [movies[i:i + n] for i in range(0, len(movies),n)]
    return render_template('index.html',movies=sublists)

@public.route('/found', methods=['POST'])
def recomendation():
    m_name = " ".join(request.form['movie_name'].split())
    result_final = recomender.recomend(m_name)
    movie = recomender.get_movie_data(m_name)
    return render_template('found.html',movies=result_final,search=movie[0])

@public.route("/keywords",methods=['POST'])
def keywords_recomendation():
    if  request.method == 'POST':
        keywords = " ".join(request.form['keywords'].split())
        result_final = recomender.get_keyword_recomendation(keywords)
        return render_template('found.html',movies=result_final,search_name=keywords)
    

@public.route("/profile",methods=['GET'])    
@login_required
def profile():
    form = ReviewForm()
    return render_template("profile.html",form=form)

@public.route("/profile/add/<id>",methods=['GET'])
@login_required
def watchlist_add(id):
    movie = Movie.query.filter_by(id=id).first()
    if movie not in current_user.watchlist:
        current_user.watchlist.append(movie)
    db.session.commit()
    return redirect(url_for("public.profile"))

@public.route("/profile/del/<id>",methods=['GET'])
@login_required
def watchlist_del(id):
    movie = Movie.query.filter_by(id=id).first()
    if movie in current_user.watchlist:
        current_user.watchlist.remove(movie)
    db.session.commit()
    return redirect(url_for("public.profile"))


@public.route("/profile/add/review",methods=['POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        movie_id = form.movie_ID.data
        rating = form.rating.data
        review_text = form.review_text.data
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie:
            review = Review(User_ID = current_user.id,Movie_ID=movie.index,rating=rating,review_text=review_text)
            current_user.reviews.append(review)
            db.session.commit()
    return redirect(url_for("public.profile"))


@public.route("/profile/del/review/<id>",methods=['GET'])
@login_required
def del_review(id):
    review = Review.query.filter_by(Review_ID=id).first()
    if review in current_user.reviews:
        Review.query.filter_by(Review_ID = id).delete()
        db.session.commit()
    return redirect(url_for("public.profile"))