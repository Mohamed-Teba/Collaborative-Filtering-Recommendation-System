import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np

data_path = "Collaborative-Filtering-Recommender/data"
ratings = pd.read_csv(f"{data_path}/u_data.csv", sep='\t', names=["user_id", "item_id", "rating", "timestamp"])
movies = pd.read_csv(f"{data_path}/u_item.csv", sep='|', encoding='latin-1', header=None, usecols=[0, 1], names=["item_id", "title"])
users = pd.read_csv(f"{data_path}/u_user.csv", sep='|', encoding='latin-1', header=None, names=["user_id", "age", "gender", "occupation", "zip_code"])

ratings = ratings.merge(movies, on="item_id")

user_item_matrix = ratings.pivot_table(index='user_id', columns='title', values='rating')

user_item_matrix_filled = user_item_matrix.fillna(0)

user_similarity = cosine_similarity(user_item_matrix_filled)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def get_user_recommendations(user_id, num_recommendations=5):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
    weighted_ratings = user_item_matrix.loc[similar_users.index].T.dot(similar_users)
    sum_similarities = similar_users.sum()
    if sum_similarities > 0:
        recommendations = weighted_ratings / sum_similarities
    else:
        recommendations = weighted_ratings

    watched_movies = user_item_matrix.loc[user_id].dropna().index
    recommendations = recommendations.drop(labels=watched_movies, errors='ignore')

    return recommendations.sort_values(ascending=False).head(num_recommendations)

recommended_movies = get_user_recommendations(10, 5)
print("Top 5 movie recommendations for User 10:")
print(recommended_movies)
