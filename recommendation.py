import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bson import ObjectId

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
client = MongoClient("mongodb+srv://dubeydon:xdksLmXEcsX_Zm9@cluster0.zrmmdlj.mongodb.net/musicmania?retryWrites=true&w=majority&appName=Cluster0")
db = client.musicmania

def fetch_user_data(user_id):
    try:
        # Convert user_id to ObjectId if necessary
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user_id")
        
        user_id = ObjectId(user_id)
        
        # Fetch user's playlist and language preferences from the users collection
        user = db['users'].find_one({'_id': user_id}, {'playlist': 1, 'language': 1})
        
        if user is None:
            raise ValueError("User not found")
        
        # Fetch play counts from the usersongplays collection
        user_plays = list(db['usersongplays'].find({'user': user_id}))
        
        return user, pd.DataFrame(user_plays)
    
    except Exception as e:
        raise ValueError(f"Error fetching user data: {str(e)}")
    

def fetch_songs_from_db():
    # Fetch all songs data from MongoDB
    songs_collection = db['songs']
    songs = list(songs_collection.find({}, {'_id': 1, 'name': 1, 'artist': 1, 'album': 1, 'popularity': 1, 'language': 1, 'fileName': 1, 'duration': 1, 'artworkImage': 1}))
    return pd.DataFrame(songs)

def recommend_songs(user_id):
    # Fetch user data (playlist, language) and play counts
    user, user_plays_df = fetch_user_data(user_id)
    
    # Fetch all songs data
    songs_df = fetch_songs_from_db()

    # If user's language preference is empty, fetch all songs, else filter by language
    if user['language']:
        filtered_songs_df = songs_df[songs_df['language'].isin(user['language'])]
    else:
        filtered_songs_df = songs_df  # No language preference, consider all songs
    
    # One-hot encode for categorical variables (artist, language)
    df_encoded = pd.get_dummies(filtered_songs_df[['artist', 'language']])
    # Add popularity as an important feature in encoding
    df_encoded['popularity'] = filtered_songs_df['popularity']
    
    # If there are no user plays, create an empty DataFrame with similar columns for merging
    if user_plays_df.empty:
        user_plays_df = pd.DataFrame(columns=['_id', 'play_count'])
    else:
        # Rename columns for merging
        user_plays_df = user_plays_df.rename(columns={'_id': 'play_id', 'song': '_id', 'count': 'play_count'})
    
    # Merge play counts with songs data
    filtered_songs_df = pd.merge(filtered_songs_df, user_plays_df, on='_id', how='left').fillna(0)
    
    # Add play_count as an important feature in encoding
    df_encoded['play_count'] = filtered_songs_df['play_count']

    # Fill NaN values with 0
    df_encoded = df_encoded.fillna(0)

    # Check if df_encoded is empty (no data to process)
    if df_encoded.empty:
        return []  # Return empty list if no data is available for recommendation

    # Compute similarity matrix using cosine similarity
    similarity_matrix = cosine_similarity(df_encoded)
    
    recommendations = []
    # If user has a playlist, recommend based on it
    if user['playlist']:
        for song_id in user['playlist']:
            if song_id in filtered_songs_df['_id'].values:
                song_index = filtered_songs_df[filtered_songs_df['_id'] == song_id].index[0]
                similarity_scores = list(enumerate(similarity_matrix[song_index]))
                similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
                top_songs_indices = [i[0] for i in similarity_scores[1:4]]
                recommendations.extend(filtered_songs_df.iloc[top_songs_indices]['_id'].values)
    else:
        # If no playlist, recommend the most popular songs in user's preferred language
        recommendations = filtered_songs_df.sort_values(by='popularity', ascending=False).head(3)['_id'].values

    # Convert recommendations to list of dictionaries
    recommended_songs = filtered_songs_df[filtered_songs_df['_id'].isin(recommendations)].to_dict('records')

    # Convert ObjectId to string for JSON serialization
    for song in recommended_songs:
        for key, value in song.items():
            if isinstance(value, ObjectId):
                song[key] = str(value)

    # Return recommended songs
    return recommended_songs

if __name__ == '__main__':
    user_id = '667bbe14acdd9c38ec325d43'  # Example user_id
    recommendations = recommend_songs(user_id)
    print(recommendations)