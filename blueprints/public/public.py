from flask import Blueprint,redirect,render_template,url_for,request
import Recomender as Recomender

recomender = Recomender.MovieRecomender("cleaned_10000.csv")
recomender.select_features(['cast','director','keywords','overview','genres','title'])
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