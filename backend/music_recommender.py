import os
import json

# Definir la ubicación base del script para acceder a los archivos de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_music_data():
    # Rutas relativas a los archivos de datos JSON
    music_data_path = os.path.join(BASE_DIR, '..', 'data', 'music_data.json')
    personalities_data_path = os.path.join(BASE_DIR, '..', 'data', 'genres_personalities.json')
    mood_genres_path = os.path.join(BASE_DIR, '..', 'data', 'mood_genres.json')

    # Cargar los datos desde los archivos JSON
    with open(music_data_path, encoding='utf-8') as file:
        music_data = json.load(file)
    with open(personalities_data_path, encoding='utf-8') as file:
        personalities_data = json.load(file)
    with open(mood_genres_path, encoding='utf-8') as file:
        mood_genres = json.load(file)
    return music_data, personalities_data, mood_genres

# Cargar los datos al iniciar el módulo
music_data, personalities_data, mood_genres = load_music_data()

def get_genres_by_personality(personality, personalities_data):
    # Obtener los géneros musicales asociados a una personalidad
    genres = []
    for genre, personalities in personalities_data.items():
        if personality.lower() in [p.lower() for p in personalities]:
            genres.append(genre)
    return genres

def get_combined_genres(personality_genres, mood_genres, mood):
    # Combinar géneros de personalidad y estado de ánimo
    mood_related_genres = mood_genres.get(mood, [])
    combined_genres = list(set(personality_genres).intersection(set(mood_related_genres)))
    return combined_genres if combined_genres else list(set(personality_genres + mood_related_genres))

def retrieve_data(data, genres):
    # Obtener recomendaciones basadas en géneros combinados
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

def generate_response(user_personality, user_mood):
    # Generar respuesta de recomendaciones basada en la personalidad y el estado de ánimo del usuario
    personality_genres = get_genres_by_personality(user_personality, personalities_data)
    combined_genres = get_combined_genres(personality_genres, mood_genres, user_mood)
    relevant_data = retrieve_data(music_data, combined_genres)
    response = "Aquí están tus recomendaciones de canciones y artistas basadas en tu personalidad y estado de ánimo:\n"
    for i, (artist, info) in enumerate(relevant_data.items(), start=1):
        response += f"{i}. Canción: {info['song']}, Artista: {artist}\n"
    return response, relevant_data

def query_artist_bio(artist_index, recommendations):
    # Consultar la biografía de un artista basado en el índice proporcionado
    try:
        if 0 <= artist_index < len(recommendations):
            artist_name = list(recommendations.keys())[artist_index]
            artist_bio = recommendations[artist_name]['bio']
            return f"Biografía de {artist_name}:\n{artist_bio}"
        else:
            return "Número de artista inválido. Por favor, ingresa un número válido."
    except ValueError:
        return "Entrada inválida. Por favor, ingresa un número válido."
