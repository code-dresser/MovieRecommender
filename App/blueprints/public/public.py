from flask import Blueprint,redirect,render_template,url_for,request,jsonify
from ...Models import Movie
from  ... import Recomender
from ...extentions import db
from ...forms import ReviewForm
recommender = Recomender.MovieRecommender(r"App\top25000_tmdb.csv",tfidf=True)
recommender.vectorize(['title', 'tagline', 'genres', 'cast', 'director', 'writers', 'producers'])
public = Blueprint("public", __name__,template_folder="templates/public")

# Index page
@public.route('/', methods=['GET'])
def main():
    # Number of items per sublist 
    n = 3 
    movies = []
    for id in recommender.get_popular_movies():
        movie = Movie.query.filter(Movie.id == id).first_or_404()
        poster_path = "https://image.tmdb.org/t/p/original" + movie.poster_path if movie.poster_path != "" else url_for('static','default-movie.png')
        movies.append([movie.title,"{:.2f}".format(movie.vote_average),movie.tagline,movie.id,poster_path])
    # Create sublist using list comprehension
    sublist = [movies[i:i + n] for i in range(0, len(movies),n)]
    return render_template('index.html',movies=sublist)

# Search results
@public.route('/found', methods=['GET'])
def recommendation():
    form = ReviewForm()
    prompt = " ".join(request.args.get('prompt',"",type=str).split()).lower()
    if prompt != "":
        if prompt in recommender.movie_data['title'].to_list():
            # Movies recommendation
            print(prompt,type(prompt))
            result_final = db.session.query(Movie).filter(Movie.id.in_(recommender.recommend(prompt))).all()
            # Searched movie
            search = Movie.query.filter_by(id = recommender.get_movie_id(prompt))
            reviews = Movie.query.filter_by(title = prompt).first().reviews
            return render_template('found.html',movies=result_final,search=search,reviews=reviews[:5],form=form)
        else:
            result_final = db.session.query(Movie).filter(Movie.id.in_(recommender.get_keyword_recommendations(prompt))).all()
            return render_template('found.html',movies=result_final,search_name=prompt.capitalize())
    else:
        return redirect(url_for("public.main"))


# Generate title list for autocompletion
@public.route("/titles")
def get_titles():
    return jsonify(recommender.get_suggestions())
  