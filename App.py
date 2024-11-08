import flask
import Recomender
recomender = Recomender.MovieRecomender("cleaned_10000.csv")
recomender.select_features(['cast','director','keywords','overview','genres','title'])
recomender.vectorise()
app = flask.Flask(__name__, template_folder='templates')
# Set up the main route
@app.route('/', methods=['GET'])
def main():
    # Number of items per sublist 
    n = 3 
    movies = recomender.get_popular_movies()
    # Create sublists using list comprehension 
    sublists = [movies[i:i + n] for i in range(0, len(movies),n)]
    return flask.render_template('index.html',movies=sublists)

@app.route('/found', methods=['POST'])
def recomendation():
    m_name = " ".join(flask.request.form['movie_name'].split())
    result_final = recomender.recomend(m_name)
    movie = recomender.get_movie_data(m_name)
    return flask.render_template('found.html',movies=result_final,search=movie[0])

@app.route("/keywords",methods=['POST'])
def keywords_recomendation():
    if flask.request.method == 'POST':
        keywords = " ".join(flask.request.form['keywords'].split())
        result_final = recomender.get_keyword_recomendation(keywords)
        return flask.render_template('found.html',movies=result_final,search_name=keywords)
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
