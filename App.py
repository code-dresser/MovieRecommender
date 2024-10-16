import flask
import Recomender
recomender = Recomender.MovieRecomender("movies10000.csv")
recomender.select_features(["Overview","Genres","Cast","Crew",'Tagline'])
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


@app.route("/keywords",methods=['POST'])
def keywords_recomendation():
    if flask.request.method == 'POST':
        keywords = " ".join(flask.request.form['keywords'].split())
        result_final = recomender.get_keyword_recomendation(keywords)
        return flask.render_template('found.html',movies=result_final,search_name=keywords)
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run()
