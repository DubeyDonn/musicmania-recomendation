# MusicMania Recommendation System

This project is a music recommendation system that uses user data and song features to recommend songs to users based on their preferences and listening history.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3.8 or later installed.
- You have `pip` installed.
- You have access to a MongoDB instance.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/musicmania-recommendation.git
   cd musicmania-recommendation
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

4. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. Update the MongoDB connection string in the [`recommendation.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FD%3A%2FProjects%2Fmusicmania-recomendation%2Frecommendation.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "d:\\Projects\musicmania-recomendation\recommendation.py") file:

   ```python
   client = MongoClient("your_mongodb_connection_string")
   ```

## Running the Application

1. Start the Flask application:

   ```sh
   python app.py
   ```

2. The application will be available at `http://127.0.0.1:5000`.

## Usage

To get song recommendations for a user, make a GET request to the `/recommend` endpoint with the `user_id` as a query parameter:

```sh
curl http://127.0.0.1:5000/recommend?user_id=<user_id>
```
