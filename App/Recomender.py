import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tmdbv3api import TMDb, Movie
from dotenv import load_dotenv
import os

class MovieRecomender:

    def __init__(self,movie_data,tfidf=True) -> None:
        self.vectorizer = TfidfVectorizer(stop_words='english',analyzer='word') if tfidf else CountVectorizer(stop_words="english")
        self.movie_data = pd.read_csv(movie_data)
        self.tfid_vector = []
        self.similarity_matrix = []
        self.features = ''
        self.title_list = self.movie_data['title'].tolist()
        self.tmdb = TMDb()
        load_dotenv()
        self.tmdb.api_key = os.getenv("TMDB_API_KEY") 
        pass
    

    def get_popular_movies(self) :
        movie_indices = self.movie_data.sort_values("score",ascending=False).head(9)
        return movie_indices['id'].values.tolist()
        
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


    def recomend(self,title:str,recomendations:int=6) -> list:
        find_match = difflib.get_close_matches(title,self.title_list)[0]
        index_of_the_movie = self.movie_data[self.movie_data.title == find_match]['index'].values[0]
        similarity_score = list(enumerate(self.similarity_matrix[index_of_the_movie ]))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[1:recomendations+1]
        movie_indices = [ int(self.movie_data[['id']].iloc[i[0]].values) for i in results] 
        return movie_indices


    def get_keyword_recomendation(self,keywords :str,recomendations:int=6) -> list:
        keywords = keywords.split()
        keywords = " ".join(keywords)
        vector = self.vectorizer.transform([keywords])
        similarity = cosine_similarity(vector,self.tfid_vector)[0]
        similarity_score = list(enumerate(similarity))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[1:recomendations+1]
        movie_indices = [ int(self.movie_data[['id']].iloc[i[0]].values) for i in results]        
        return movie_indices

    def get_suggestions(self) -> list:
        return self.movie_data['title'].str.title().tolist()
    
    def get_movie_id(self,  title :str) -> list:
        find_match = difflib.get_close_matches(title,self.title_list)[0]
        index_of_the_movie = self.movie_data[self.movie_data.title == find_match]['index'].values[0]
        movie = self.movie_data["id"].iloc[index_of_the_movie]
        return int(movie)
    

    
# recomender = MovieRecomender("movies10000.csv")
# recomender.select_features(["overview","genres","Cast","Crew",'Tagline'])
# recomender.vectorise()
# # # print(recomender.get_suggestions())
# result = recomender.recomend(input("What is yours favourite movie:  "))
# for r in result:
#     print(r[0])
# result = recomender.get_keyword_recomendation("Christopher Nolan")
# for r in result:
#     print(r[0])