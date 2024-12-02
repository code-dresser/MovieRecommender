from flask import Blueprint,redirect,render_template,url_for,request,jsonify,flash
from flask_login import login_required,current_user
from ...Models import Movie,Review,User
from  ... import Recomender
from ...extentions import db
from .forms import ReviewForm
import random
recomender = Recomender.MovieRecomender(r"App\top25000_tmdb.csv",False)
recomender.select_features(['title','tagline','genres','cast','director','writers','producers'])
recomender.vectorise()
public = Blueprint("public", __name__,template_folder="templates/public")

# Index page
@public.route('/', methods=['GET'])
def main():
    # Number of items per sublist 
    n = 3 
    movies = []
    for id in recomender.get_popular_movies():
        movie = Movie.query.filter(Movie.id == id).first_or_404()
        poster_path = "https://image.tmdb.org/t/p/original" + movie.poster_path if movie.poster_path != "" else url_for('static','default-movie.png')
        movies.append([movie.title,"{:.2f}".format(movie.vote_average),movie.tagline,movie.id,poster_path])
    # Create sublists using list comprehension 
    sublists = [movies[i:i + n] for i in range(0, len(movies),n)]
    return render_template('index.html',movies=sublists)

# Search results
@public.route('/found', methods=['POST'])
def recomendation():
    prompt = " ".join(request.form['movie_name'].split()).lower()
    if prompt in recomender.title_list:
        # Movies recomendation
        result_final = movie_info(recomender.recomend(prompt))
        # Searched movie
        search = movie_info(recomender.get_movie_id(prompt))
        reviews = Movie.query.filter_by(title = prompt).first().reviews
        return render_template('found.html',movies=result_final,search=search,reviews=reviews[:5])
    else:
        result_final = movie_info(recomender.get_keyword_recomendation(prompt))
        return render_template('found.html',movies=result_final,search_name=prompt.capitalize())


@public.route("/user/<username>",methods=['GET'])    
def user(username):
    user = User.query.filter(User.Username == username).first_or_404()
    return render_template("user_page.html",user=user)

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

@public.route("/profile/add/movie",methods=['POST'])
@login_required
def post_watchlist():
    if request.form['movie']:
        movie = Movie.query.filter_by(title = request.form['movie'].lower()).first_or_404()
        if movie:
            if movie not in current_user.watchlist:
                current_user.watchlist.append(movie)
                db.session.commit()
            else:
                flash("Movie already in watchlist")
        else:
            flash("Error occured while adding the movie")
        return render_template("_profile_watchlist.html")
    
@public.route("/profile/del/<id>",methods=['GET'])
@login_required
def watchlist_del(id):
    movie = Movie.query.filter_by(id=id).first_or_404()
    if movie in current_user.watchlist:
        current_user.watchlist.remove(movie)
    db.session.commit()
    return render_template("_profile_watchlist.html")


@public.route("/profile/add/review",methods=['POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        movie_id = form.movie_ID.data
        title= form.title.data
        rating = form.rating.data
        review_text = form.review_text.data
        movie = Movie.query.filter_by(id=movie_id).first_or_404()
        if movie:
            review = Review(User_ID = current_user.id,Movie_ID=movie.index,title=title,rating=rating,review_text=review_text)
            current_user.reviews.append(review)
            db.session.commit()
        else:
            flash("Unable to add movie to db")
    else:
        flash("Form not validated")
    return redirect(url_for("public.profile"))


@public.route("/profile/del/review/<id>",methods=['GET'])
@login_required
def del_review(id):
    review = Review.query.filter_by(Review_ID=id).first_or_404()
    if review in current_user.reviews:
        Review.query.filter_by(Review_ID = id).delete()
        db.session.commit()
    return render_template("_profile_reviews.html")




@public.route("/titles")
def get_titles():
    return jsonify(recomender.get_suggestions())

def movie_info(ids: list) -> list:
    if isinstance(ids,list):
        result = []
        for id in ids:
            movie = Movie.query.filter(Movie.id == id).first()
            if movie:
                poster_path = "https://image.tmdb.org/t/p/original" + movie.poster_path if movie.poster_path != "" else url_for('static',filename='default-movie.png')
                result.append([movie.title,"{:.2f}".format(movie.vote_average),movie.genres,movie.overview,movie.id,poster_path])
        return result
    else:
        movie = Movie.query.filter(Movie.id == ids).first()
        print(movie)
        if movie:
            poster_path = "https://image.tmdb.org/t/p/original" + movie.poster_path if movie.poster_path != "" else url_for('static',filename='default-movie.png')
            result = [movie.title,"{:.2f}".format(movie.vote_average),movie.genres,movie.overview,movie.id,poster_path]
            return result   