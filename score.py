import numpy as np
import pandas as pd

def datafile() :
    datafile1 = pd.read_csv("tmdb_5000_credits.csv")
    datafile2 = pd.read_csv("tmdb_5000_movies.csv")

    datafile1.columns = ['id', 'title', 'cast', 'crew']
    datafile = datafile2.merge(datafile1, on='id')
    return datafile

def score() :
    data = datafile()
    mean = data['vote_average'].mean()
    quantile = data['vote_count'].quantile(0.8)
    q_movies = data.copy().loc[data['vote_count'] >= quantile]


#   weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
#   R = average for the movie (mean) = (Rating)
#   v = number of votes for the movie = (votes)
#   m (quantile) = minimum votes required to be listed in the Top 250 (currently 3000)
#   C (mean) = the mean vote across the whole report (currently 6.9)
    def weighted_rating(x, quantile=quantile, mean=mean):
        v = x['vote_count']
        R = x['vote_average']

        return (v / (v + quantile) * R) + (quantile / (quantile + v) * mean)

    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

    q_movies=q_movies.sort_values(by='score', ascending=False)
    print(q_movies.head(10)[['title_y', 'vote_count', 'vote_average', 'score']])

    return q_movies