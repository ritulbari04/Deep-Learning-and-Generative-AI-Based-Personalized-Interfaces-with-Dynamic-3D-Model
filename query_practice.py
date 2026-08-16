import os
import weaviate
import google.generativeai as genai
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
genai.configure(api_key="AIzaSyC3pCAiP_jYxMrYO8C6alZzCYTrP11EE8A")
history = dict()

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "This is home page"

@app.route('/ask/<string:query>')
def want_answer(query):
    model1 = genai.GenerativeModel("gemini-1.5-flash")
    response = model1.generate_content(
        f"Given a chat history that is {history} and the latest user question that is {query} which might reference context in the chat history. Formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as it is."
    )

    query = response.text

    response = questions.generate.near_text(
        query=query,
        limit=5,
        grouped_task=f"Answer the question {query} in simple Indian English as a teacher."
    )

    from_rag = response.generated

    model2 = genai.GenerativeModel("gemini-1.5-flash")
    response = model2.generate_content(
        f"You are a teacher, teaching a student and giving a mature and simplified answer in easy English. It should be in 100 words. The query asked by the student is {query}. Here is an output from a RAG model: {from_rag}. It can be right or wrong; you should answer accordingly. Don't reveal that you are using any reference and don't use special characters like '*'. Only use paragraph format."
    )

    mytext = response.text
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

