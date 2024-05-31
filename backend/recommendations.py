import json

# Cargar los datos de música y personalidades
def load_music_data():
    with open('../data/music_data.json', encoding='utf-8') as file:
        music_data = json.load(file)
    with open('../data/genres_personalities.json', encoding='utf-8') as file:
        personalities_data = json.load(file)
    with open('../data/mood_genres.json', encoding='utf-8') as file:
        mood_genres = json.load(file)
    return music_data, personalities_data, mood_genres

# Obtener los géneros asociados a una personalidad
def get_genres_by_personality(personality, personalities_data):
    genres = []
    for genre, personalities in personalities_data.items():
        if personality.lower() in [p.lower() for p in personalities]:
            genres.append(genre)
    return genres

# Combinar géneros de personalidad y estado de ánimo
def get_combined_genres(personality_genres, mood_genres, mood):
    mood_related_genres = mood_genres.get(mood, [])
    combined_genres = list(set(personality_genres).intersection(set(mood_related_genres)))
    return combined_genres if combined_genres else list(set(personality_genres + mood_related_genres))

# Obtener recomendaciones basadas en los géneros combinados
def retrieve_data(data, genres):
    recommendations = {}
    artists_seen = set()
    for genre in genres:
        for artist in data:
            if artist['name'] in artists_seen:
                continue
            for album in artist['albums']:
                if genre.lower() in [g.lower() for g in album['genres']]:
                    if artist['name'] not in artists_seen:
                        recommendations[artist['name']] = {
                            'song': album['name'],
                            'artist': artist['name'],
                            'bio': artist['bio']
                        }
                        artists_seen.add(artist['name'])
                        break
            if len(recommendations) >= 10:
                break
        if len(recommendations) >= 10:
            break
    return recommendations

# Generar respuesta de recomendaciones
def generate_response(user_personality, user_mood, music_data, personalities_data, mood_genres):
    personality_genres = get_genres_by_personality(user_personality, personalities_data)
    combined_genres = get_combined_genres(personality_genres, mood_genres, user_mood)
    relevant_data = retrieve_data(music_data, combined_genres)
    response = "Aquí están tus recomendaciones de canciones y artistas basadas en tu personalidad y estado de ánimo:\n"
    for i, (artist, info) in enumerate(relevant_data.items(), start=1):
        response += f"{i}. Canción: {info['song']}, Artista: {artist}\n"
    return response, relevant_data