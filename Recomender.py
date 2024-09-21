import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tmdbv3api import TMDb, Movie


class MovieRecomender:

    def __init__(self,movie_data) -> None:
        self.movie_data = pd.read_csv(movie_data)
        self.similarity_matrix = []
        self.features = ''
        self.title_list = self.movie_data['title'].tolist()
        self.tmdb = TMDb()
        self.tmdb.api_key = "1cdf6c52a3c228e5f6cb4d02386e54e7"
        pass

    def load_movie_data(self,path :str) -> None:
        self.movie_data = pd.read_csv(path)
        pass

    def select_features(self, feature_list :list) -> None:
        for feature in feature_list:
            self.movie_data[feature] = self.movie_data[feature].fillna('')

        for feature in feature_list:
            self.features += self.movie_data[feature] + ' '
        pass

    def vectorise(self):
        vectorizer = TfidfVectorizer(stop_words='english',analyzer='word')
        tfid_vector = vectorizer.fit_transform(self.features)
        self.similarity_matrix = cosine_similarity(tfid_vector)
        pass


    def recomend(self,title,recomendations=5):
        find_match = difflib.get_close_matches(title,self.title_list)[0]
        index_of_the_movie = self.movie_data[self.movie_data.title == find_match]['index'].values[0]
        similarity_score = list(enumerate(self.similarity_matrix[index_of_the_movie ]))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[1:recomendations+1]
        movie_indices = [self.movie_data[['title','vote_average','genres','tagline','id']].iloc[i[0]] for i in results]
        recomendations = []
        for rec in movie_indices:
            movie = Movie()
            search = movie.search(rec.iloc[0])
            if search:
                details = movie.details(rec.iloc[-1])
                poster_path = details.poster_path
                base_url = 'https://image.tmdb.org/t/p/original'
                poster_url = pd.Series(f"{base_url}{poster_path}")
                rec = pd.concat([rec,poster_url],ignore_index=True)
                recomendations.append(rec)
                
        return recomendations

        # for i in range(recomendations):
        #     movie = sorted_similarity[i+1]
        #     index = movie[0]
        #     title_from_index = self.movie_data[self.movie_data.index == index]['title'].values[0]
        #     print(i, '.', title_from_index)

    def get_suggestions(self):
        return self.movie_data['title'].str.capitalize().tolist()
    
# recomender = MovieRecomender("movies.csv")
# recomender.select_features(['genres', 'keywords', 'tagline', 'cast', 'director'])
# recomender.vectorise()
# # print(recomender.get_suggestions())
# result = recomender.recomend(input("What is yours favourite movie:  "))
# print(result[0]['title'])