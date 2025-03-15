import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self,movie_data,tfidf=True) -> None:
        self.vectorizer = TfidfVectorizer(stop_words='english',analyzer='word') if tfidf else CountVectorizer(stop_words="english", analyzer='word')
        self.movie_data = pd.read_csv(movie_data)
        self.tfidf_vector = []
        self.similarity_matrix = []
        #mean vote across the whole report
        self.C = self.movie_data['vote_average'].mean()
        # Minimum votes required to be listed in the chart
        # I'm using 90 percentile as my cutoff
        # i.e. for the movie to be listed it must have more votes than at least 90% of the movies in the list
        self.m = self.movie_data['vote_count'].quantile(0.9)
        self.preprocess_df(movie_data)
        pass
    
    
    def preprocess_df(self,filename):
        if "index" not in self.movie_data.columns:
            self.movie_data = self.movie_data.reset_index()
        if "score" in self.movie_data.columns:
            pass
        else:
            self.movie_data["score"] = self.movie_data.apply(self.weighted_ratings,axis=1)
            self.movie_data.to_csv(filename,index=False)
            pass
        
    def weighted_ratings(self,x):
        v = x['vote_count']  # No. of voted for the movie
        R = x['vote_average']  # Average rating for the movie
        # Calculation based on teh IMDB formula
        return (v/v+self.m) * R + (self.m/self.m+v) * self.C
    # Weighed Rating (WR) = ((v/v+m) * R + (m/m+v) * C)
    # v = number of votes for the movie;
    # m = minimum votes required to be listed in the chart;
    # R = average rating of the movie; And
    # C = mean vote across the whole report
        
    def get_popular_movies(self) :
        movie_indices = self.movie_data.sort_values("score",ascending=False).head(9)
        return movie_indices['id'].values.tolist()
        
    def vectorize(self, feature_list :list) -> None:
        features = ''
        for feature in feature_list:
            self.movie_data[feature] = self.movie_data[feature].fillna('')
            features += self.movie_data[feature] + ' '
        self.tfidf_vector = self.vectorizer.fit_transform(features)
        self.similarity_matrix = cosine_similarity(self.tfidf_vector, self.tfidf_vector)
        pass


    def recommend(self, title:str, recommendations:int=6) -> list:
        index_of_the_movie = self.movie_data[self.movie_data.title == title]['index'].values[0]
        similarity_score = list(enumerate(self.similarity_matrix[index_of_the_movie ]))
        sorted_similarity = sorted(similarity_score,key=lambda x: x[1],reverse=True)
        results = sorted_similarity[1:recommendations + 1]
        movie_indices = self.movie_data['id'].iloc[[i[0] for i in results]].tolist()
        return movie_indices

    def get_keyword_recommendations(self, keywords: str, recommendations: int = 6) -> list:
        keywords = keywords.split()
        keywords = " ".join(keywords)
        vector = self.vectorizer.transform([keywords])
        similarity = cosine_similarity(vector, self.tfidf_vector)[0]
        similarity_score = list(enumerate(similarity))
        sorted_similarity = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        # Filter out movies with vote_count < mean vote count
        filtered_results = [(idx, score) for idx, score in sorted_similarity if self.movie_data['vote_count'].iloc[idx] >= self.movie_data['vote_count'].mean() ]
        results = filtered_results[:recommendations]
        movie_indices = self.movie_data['id'].iloc[[i[0] for i in results]].tolist()
        
        return movie_indices


    def get_suggestions(self) -> list:
        return self.movie_data['title'].str.title().tolist()
    
    def get_movie_id(self,  title :str) -> int:
        index_of_the_movie = self.movie_data[self.movie_data.title == title]['index'].values[0]
        movie = self.movie_data["id"].iloc[index_of_the_movie]
        return int(movie)
    