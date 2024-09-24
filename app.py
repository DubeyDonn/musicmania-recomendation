from flask import Flask, jsonify, request
from recommendation import fetch_songs_from_db, recommend_songs

app = Flask(__name__)

# Endpoint to get recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    song_id = request.args.get('song_id')
    
    # Fetch song data and get recommendations
    songs_df = fetch_songs_from_db()
    recommendations = recommend_songs(song_id, songs_df)
    
    # Convert recommendations to JSON format
    recommended_songs = recommendations[['name', 'artist', 'album', 'popularity']].to_dict('records')
    return jsonify(recommended_songs)

if __name__ == '__main__':
    app.run(debug=True)
