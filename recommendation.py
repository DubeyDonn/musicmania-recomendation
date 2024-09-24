import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://dubeydon:xdksLmXEcsX_Zm9@cluster0.zrmmdlj.mongodb.net/musicmania?retryWrites=true&w=majority&appName=Cluster0")
db = client.musicmania

def fetch_songs_from_db():
    # Fetch songs data from MongoDB
    songs_collection = db['songs']
    songs = list(songs_collection.find({}, {'_id': 1, 'name': 1, 'artist': 1, 'album': 1, 'popularity': 1, 'language': 1}))
    return pd.DataFrame(songs)

def recommend_songs(song_id, song_df):
    # One-hot encoding for categorical variables (artist, language, etc.)
    df_encoded = pd.get_dummies(song_df[['artist', 'language']])
    df_encoded['popularity'] = song_df['popularity']
    
    # Compute similarity matrix using cosine similarity
    similarity_matrix = cosine_similarity(df_encoded)
    
    # Find index of the given song_id
    song_index = song_df[song_df['_id'] == song_id].index[0]
    
    # Get similarity scores for the song
    similarity_scores = list(enumerate(similarity_matrix[song_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 3 most similar songs
    top_songs_indices = [i[0] for i in similarity_scores[1:4]]
    return song_df.iloc[top_songs_indices]

if __name__ == '__main__':
    # Example to fetch songs and make recommendations
    songs_df = fetch_songs_from_db()
    recommendations = recommend_songs('668115d78eb9444db49dd6f8', songs_df)
    print(recommendations[['name', 'artist', 'album', 'popularity']])
