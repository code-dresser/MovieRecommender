from flask import Blueprint,redirect,render_template,url_for,request,jsonify,flash
from flask_login import login_required,current_user
from ...Models import Movie,Review,User
from  ... import Recomender
from ...extentions import db
from ...forms import ReviewForm
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
            result_final = db.session.query(Movie).filter(Movie.id.in_(recomender.get_keyword_recomendation(prompt))).all()
            return render_template('found.html',movies=result_final,search_name=prompt.capitalize())
    else:
        return redirect(url_for("public.main"))


# Generate title list for autocompletion
@public.route("/titles")
def get_titles():
    return jsonify(recomender.get_suggestions())
  