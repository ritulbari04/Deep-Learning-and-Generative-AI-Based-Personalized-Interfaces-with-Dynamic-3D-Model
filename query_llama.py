import os
import weaviate
import ollama
import asyncio
import edge_tts
from flask import Flask, jsonify, send_file
from flask_cors import CORS  # Allow frontend to call backend

# Async TTS generation
async def get_voice(text):
    output_path = os.path.join("static", "output.mp3")
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural", rate="+10%")
    await communicate.save(output_path)
    print("Audio saved as", output_path)

# Weaviate + Gemini setup
client = weaviate.connect_to_local()
questions = client.collections.get("School")
history = dict()

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "This is home page"

@app.route('/ask/<string:query>')
def want_answer(query):
    model1 = ollama.chat(
        model='llama3.2',  # Or 'llama3.2' if you named it that
        messages=[
            {'role': 'user', 'content': f"Given a chat history that is {history} and the latest user question that is {query} which might reference context in the chat history. Formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and if No changes are needed to the question just return it as it is"}
        ]
    )

    query=model1['message']['content']

    response = questions.generate.near_text(
        query=query,
        limit=5,
        grouped_task=f"Answer the question {query} in simple Indian English as a teacher."

    )

    from_rag=response.generated

    model2 = ollama.chat(
        model='llama3.2',  # Or 'llama3.2' if you named it that
        messages=[
            {'role': 'user', 'content': f"you are a teacher, teaching a student and giving a mature and simplified answer in easy english. It should be in 100 words. the query asked by that student is{query} in english, here is an output coming from a RAG model that is {from_rag} it can be right or wrong, you should give answer accordingly. Don't reveal that you are using any reference and don't use any kind of  character like '*' and only use paragraph."}
        ]
    )
    mytext=model2['message']['content']
    history[query] = mytext

    asyncio.run(get_voice(mytext))  # Generate and save audio to static/output.mp3

    return jsonify({
        "query": query,
        "response": mytext
    })

@app.route('/audio')
def serve_audio():
    audio_path = os.path.join("static", "output.mp3")
    return send_file(audio_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    # Ensure static folder exists
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)

client.close()

