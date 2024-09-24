from flask import Flask, jsonify, request
from recommendation import fetch_songs_from_db, recommend_songs

app = Flask(__name__)

# Endpoint to get recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    # print(request.args)
    print(request.args.get('user_id'))
    user_id = request.args.get('user_id')
    
    # Fetch song data and get recommendations
    recommendations = recommend_songs(user_id)
    
    # Convert recommendations to JSON format
    # recommended_songs = recommendations[['name', 'artist', 'album', 'popularity']].to_dict('records')
    # return jsonify(recommended_songs)

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
