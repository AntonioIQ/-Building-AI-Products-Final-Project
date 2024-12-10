# -Building-AI-Music Recommender

Music Recommender 🎶🎧🎼
Find your perfect soundtrack with this personalized music recommendation engine! This project combines your personality traits and current mood to suggest new artists and songs that align with your unique style and emotions.

How it Works ⚙️
Data: Leverages JSON files (music_data.json, genres_personalities.json, mood_genres.json) containing information about artists, albums, genres, and their associations with personalities and moods.
Personality & Mood: Asks you about your personality type and current mood to tailor the recommendations.
Genre Mashup: Combines genres associated with your personality and mood to expand the possibilities.
Recommendations: Presents a list of songs and artists that match your preferences.
Dig Deeper: Lets you learn more about a selected artist, including their bio and a Q&A session powered by the Ollama language model.
How to Use 🚀
Prerequisites:

Python 3.x
Libraries: json, ollama (make sure you have a valid Ollama API key)
JSON data files mentioned above in the same directory as the script
Run:

Open your terminal and navigate to the project directory.
Execute the script: python music_recommender.py (or your filename)
Answer the questions about your personality and mood.
Explore the recommendations and query more information about artists.
Customization 🛠️
Add More Data: Expand the JSON files with more artists, albums, genres, personalities, and moods for even more diverse recommendations.
Tweak Combination Rules: Modify the get_genres_by_personality and get_combined_genres functions to experiment with different ways of combining genres.
Integrate Other Data Sources: Consider using APIs from music services (like Spotify or Last.fm) to get more up-to-date data and expand the recommendation pool.
Example Output 🎤
Here are your song and artist recommendations based on your personality and mood:
1. Song: Of Beyond, Artist: Adventure Time
2. Song: Satie: Complete Piano Works, Vol. 2/2, Artist: Erik Satie
...
Notes 📝
This project is a starting point. Feel free to customize and adapt it to your needs.
The quality of recommendations depends on the quality and quantity of data in the JSON files.
Ollama can generate additional information about artists, but its accuracy may vary.
