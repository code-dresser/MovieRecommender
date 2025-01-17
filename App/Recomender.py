import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecomender:

    def __init__(self,movie_data,tfidf=True) -> None:
        self.vectorizer = TfidfVectorizer(stop_words='english',analyzer='word') if tfidf else CountVectorizer(stop_words="english")
        self.movie_data = pd.read_csv(movie_data).reset_index()
        print(self.movie_data.head(5))
        self.tfid_vector = []
        self.similarity_matrix = []
        self.features = ''
        self.title_list = self.movie_data['title'].tolist()
        #mean vote across the whole report
        self.C = self.movie_data['vote_average'].mean()
        # Minimum votes required to be listed in the chart
        # I'm using 90 percentile as my cutoff
        # i.e. for the movie to be listed it must have more votes than at least 90% of the movies in the list
        self.m = self.movie_data['vote_count'].quantile(0.9)
        self.score_movies()
        pass
    
    
    def score_movies(self):
        if "score" in self.movie_data.columns:
            pass
        else:
            self.movie_data["score"] = self.movie_data.apply(self.weighted_ratings,axis=1)
            pass
        
    def weighted_ratings(self,x):
        v = x['vote_count']  # No. of voted for the movie
        R = x['vote_average']  # Average rating for the movie
        # Calculation based on teh IMDB formula
        return ((v/v+self.m) * R + (self.m/self.m+v) * self.C)
    # Weighed Rating (WR) = ((v/v+m) * R + (m/m+v) * C)
    # v = number of votes for the movie;
    # m = minimum votes required to be listed in the chart;
    # R = average rating of the movie; And
    # C = mean vote across the whole report
        
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