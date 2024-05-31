from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
from recommendations import load_music_data, generate_response

app = Flask(__name__)
CORS(app)

music_data, personalities_data, mood_genres = load_music_data()

# Ruta para el saludo inicial
@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_message = (
        "🎶 Hey there, music lover! 👋 I'm Echoes, your personal guide to a world of music that's uniquely you. 🎶\n\n"
        "Share your favorite tunes or artists, and let's uncover hidden gems and familiar favorites that perfectly match your vibe. Are you ready to explore the soundtrack of YOU?"
    )
    return jsonify({'response': welcome_message})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message_history = request.json.get('history')
        if not message_history:
            return jsonify({'error': 'No history provided'}), 400

        # Obtener la última pregunta del usuario desde el historial de mensajes
        user_question = message_history[-1]['content']

        # Verificar la etapa de la conversación
        if len(message_history) == 1:
            # Primera pregunta: solicitar la personalidad del usuario
            response = "Por favor, ingresa tu personalidad (extrovertido, introvertido, creativo, aventurero):"
        elif len(message_history) == 3:
            # Segunda pregunta: solicitar el estado de ánimo del usuario
            user_personality = user_question
            response = "¿Cuál es tu ánimo musical ahora? (happy, sad, energetic, relaxed, angry, romantic):"
        elif len(message_history) == 5:
            # Tercera pregunta: generar recomendaciones basadas en la personalidad y el estado de ánimo
            user_mood = user_question
            response_text, recommendations = generate_response(user_personality, user_mood, music_data, personalities_data, mood_genres)
            
            # Convertir las recomendaciones en una lista de diccionarios
            response = [
                {
                    'song': info['song'],
                    'artist': artist
                }
                for artist, info in recommendations.items()
            ]
        else:
            # Consultar sobre la biografía del artista utilizando ollama
            artist_name = user_question
            if artist_name in recommendations:
                artist_bio = recommendations[artist_name]['bio']
                prompt = f"Usuario pregunta sobre {artist_name}: {user_question}\nBiografía: {artist_bio}\nRespuesta:"
                response = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': prompt}])
                response = response['message']['content']
            else:
                response = "No se encontró información sobre el artista mencionado."

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)