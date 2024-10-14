import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tmdbv3api import TMDb, Movie


class MovieRecomender:

    def __init__(self,movie_data,tfidf=True) -> None:
        self.vectorizer = TfidfVectorizer(stop_words='english',analyzer='word') if tfidf else CountVectorizer(stop_words="english")
        self.movie_data = pd.read_csv(movie_data)
        self.tfid_vector = []
        self.similarity_matrix = []
        self.features = ''
        self.title_list = self.movie_data['Title'].tolist()
        self.tmdb = TMDb()
        self.tmdb.api_key = "1cdf6c52a3c228e5f6cb4d02386e54e7"
        pass

    def load_movie_data(self,path :str) -> None:
        self.movie_data = pd.read_csv(path)
        pass

    def select_features(self, feature_list :list) -> None:
        for feature in feature_list:
            self.movie_data[feature] = self.movie_data[feature].fillna('')
            self.features += self.movie_data[feature] + ' '
        pass

    def vectorise(self):
        self.tfid_vector = self.vectorizer.fit_transform(self.features)
        self.similarity_matrix = cosine_similarity(self.tfid_vector,self.tfid_vector)
        pass


    def recomend(self,title:str,recomendations:int=5) -> list:
        find_match = difflib.get_close_matches(title,self.title_list)[0]
        index_of_the_movie = self.movie_data[self.movie_data.Title == find_match]['index'].values[0]
        similarity_score = list(enumerate(self.similarity_matrix[index_of_the_movie ]))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[1:recomendations+1]
        movie_indices = [self.movie_data[['Title','Rating_average','Genres','Tagline','TMDb_Id']].iloc[i[0]] for i in results] 
        return self.get_movie_info(movie_indices)


    def get_keyword_recomendation(self,keywords :str,recomendations:int=5) -> list:
        keywords = keywords.split()
        keywords = " ".join(keywords)
        vector = self.vectorizer.transform([keywords])
        similarity = cosine_similarity(vector,self.tfid_vector)[0]
        similarity_score = list(enumerate(similarity))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[:5]
        movie_indices = [self.movie_data[['Title','Rating_average','Genres','Tagline','TMDb_Id']].iloc[i[0]] for i in results]          
        return self.get_movie_info(movie_indices)

    def get_suggestions(self) -> list:
        return self.movie_data['Title'].str.capitalize().tolist()
    

    def get_movie_info(self, movies :list ) -> list:
        movies_list = []
        for rec in movies:
            movie = Movie()
            search = movie.search(rec.iloc[0])
            if search:
                details = movie.details(rec.iloc[-1])
                poster_path = details.poster_path
                base_url = 'https://image.tmdb.org/t/p/original'
                poster_url = pd.Series(f"{base_url}{poster_path}")
                rec = pd.concat([rec,poster_url],ignore_index=True)
                movies_list.append(rec) 
        return movies_list
    
# recomender = MovieRecomender("movies10000.csv")
# recomender.select_features(["Overview","Genres","Cast","Crew",'Tagline'])
# recomender.vectorise()
# # # print(recomender.get_suggestions())
# result = recomender.recomend(input("What is yours favourite movie:  "))
# for r in result:
#     print(r[0])
# result = recomender.get_keyword_recomendation("Christopher Nolan")
# for r in result:
#     print(r[0])