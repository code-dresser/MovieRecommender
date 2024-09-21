import flask
import Recomender
recomender = Recomender.MovieRecomender("movies.csv")
recomender.select_features(['genres', 'keywords', 'tagline', 'cast', 'director'])
recomender.vectorise()
app = flask.Flask(__name__, template_folder='templates')
# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = " ".join(flask.request.form['movie_name'].split())
        result_final = recomender.recomend(m_name)
        return flask.render_template('found.html',movies=result_final,search_name=m_name)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
