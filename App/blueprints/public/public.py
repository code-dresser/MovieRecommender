from flask import Blueprint,redirect,render_template,url_for,request,jsonify,flash
from flask_login import login_required,current_user
from ...Models import Movie,Review,User,watchlist
from  ... import Recomender
from ...extentions import db
from .forms import ReviewForm,UserForm
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
@public.route('/found', methods=['GET'])
def recomendation():
    form = ReviewForm()
    prompt = " ".join(request.args.get('prompt',"",type=str).split()).lower()
    if prompt != "":
        if prompt in recomender.title_list:
            # Movies recomendation
            result_final = db.session.query(Movie).filter(Movie.id.in_(recomender.recomend(prompt))).all()
            # Searched movie
            search = Movie.query.filter_by(id =recomender.get_movie_id(prompt))
            reviews = Movie.query.filter_by(title = prompt).first().reviews
            return render_template('found.html',movies=result_final,search=search,reviews=reviews[:5],form=form)
        else:
            result_final = db.session.query(Movie).filter(Movie.id.in_(recomender.recomend(prompt))).all()
            return render_template('found.html',movies=result_final,search_name=prompt.capitalize())
    else:
        return redirect(url_for("public.main"))

# Public user page
@public.route("/user/<username>",methods=['GET'])    
def user(username):
    user = User.query.filter(User.Username == username).first_or_404()
    review_page = request.args.get('page',1,type=int)
    watchlist_page = request.args.get('wlist',1,type=int)
    #Pagination queries
    reviews_query = db.session.query(Review).filter(Review.User_ID == user.id)
    reviews = db.paginate(reviews_query,page=review_page,per_page=5,error_out=False)
    watchlist = db.paginate(user.watchlist_query(),page=watchlist_page,per_page=12,error_out=False)
    # Reviews navigation links
    next_url = url_for('public.user',username=user.Username,page=reviews.next_num,wlist=watchlist_page) if reviews.has_next else None
    prev_url = url_for('public.user',username=user.Username,page=reviews.prev_num,wlist=watchlist_page) if reviews.has_prev else None
    # Movies navigaiton links
    wnext_url = url_for('public.user',username=user.Username,wlist=watchlist.next_num,page=review_page) if watchlist.has_next else None
    wprev_url = url_for('public.user',username=user.Username,wlist=watchlist.prev_num,page=review_page) if watchlist.has_prev else None

    return render_template("user_page.html",user=user,reviews=reviews,next=next_url,prev=prev_url,watchlist=watchlist,w_next=wnext_url,w_prev=wprev_url)

# Private profile page
@public.route("/profile/",methods=['GET'])
@login_required
def profile():
    review_page = request.args.get('page',1,type=int)
    #pagination quary
    reviews_query = db.session.query(Review).filter(Review.User_ID == current_user.id)
    reviews = db.paginate(reviews_query,page=review_page,per_page=5,error_out=False)
    # Reviews navigation links
    next_url = url_for('public.profile',page=reviews.next_num) if reviews.has_next else None
    prev_url = url_for('public.profile', page=reviews.prev_num) if reviews.has_prev else None
    form = ReviewForm()
    u_form = UserForm()
    return render_template("profile.html",form=form,u_form=u_form,reviews=reviews,next=next_url,prev=prev_url)

#Edit user data
@public.route("/profile/edit",methods=["POST"])
@login_required
def edit_profile():
    user =  User.query.filter(User.id == current_user.id).first_or_404()
    form = UserForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.Email = form.email.data
        user.Bio = form.Bio.data
        db.session.commit()
    else:
        flash("Couldnt edit your profile info")
    return redirect(url_for("public.profile"))

# Add movies based on movie id (AJAX)
@public.route("/profile/add/<id>",methods=['GET'])
@login_required
def watchlist_add(id):
    movie = Movie.query.filter_by(id=id).first()
    if movie not in current_user.watchlist:
        current_user.watchlist.append(movie)
    db.session.commit()
    return "<i class='fas fa-heart' 'style=font-size: 2em'></i>"

#Add movie from form in profile page (AJAX)
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

# Delete movie from watchlist base on movie id
@public.route("/profile/del/<id>",methods=['GET'])
@login_required
def watchlist_del(id):
    movie = Movie.query.filter_by(id=id).first_or_404()
    if movie in current_user.watchlist:
        current_user.watchlist.remove(movie)
    db.session.commit()
    return render_template("_profile_watchlist.html")

# Add review for movie through review form
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

# Delete review base on it's id
@public.route("/profile/del/review/<id>",methods=['GET'])
@login_required
def del_review(id):
    review = Review.query.filter_by(Review_ID=id).first_or_404()
    if review in current_user.reviews:
        Review.query.filter_by(Review_ID = id).delete()
        db.session.commit()
    return render_template("_profile_reviews.html")



# Generate title list for autocompletion
@public.route("/titles")
def get_titles():
    return jsonify(recomender.get_suggestions())
  