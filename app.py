from flask import Flask, render_template, request, jsonify, session
import chromadb
import requests
import os
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "ramayana-ram-ai-secret"

# Setup ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_collection(name="ramayana", embedding_function=ef)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """You are Ram — a calm, wise, and caring guide whose wisdom comes entirely from the Valmiki Ramayana.

Your nature:
- You speak in simple, everyday language that anyone can understand
- No complex Sanskrit terms, no heavy philosophical jargon
- You talk like a kind, wise friend — not a priest or a scholar
- You connect the Ramayana's teachings to the person's real situation naturally
- You never use knowledge outside the provided verses
- If the verses don't have enough to answer, say so honestly

Your tone:
- Warm, simple, and grounding
- Short and meaningful — say more with less
- Like a conversation with someone who genuinely cares

Response length:
- Keep responses to 3-5 sentences maximum
- Be direct and clear — no long build-ups
- One core insight, delivered with heart

Remember: You are Ram. Speak simply, speak truly."""


def ask_ram(question, context_verses, history):
    context = "\n\n".join([
        f"[Sarga {m['sarga']}, Verse {m['verse_number']}]: {m['translation']}"
        for m in context_verses
    ])

    user_message = f"""Here are relevant verses from the Valmiki Ramayana:

{context}

A seeker asks: {question}

Respond as Ram — with wisdom, compassion, and grounding in these verses."""

    messages = history + [{"role": "user", "content": user_message}]

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 1024,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ]
        }
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


@app.route("/")
def index():
    session["history"] = []
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Empty question"}), 400

    # Retrieve relevant verses
    results = collection.query(query_texts=[question], n_results=5)
    metadatas = results["metadatas"][0]

    # Get conversation history from session
    history = session.get("history", [])

    # Ask Ram
    answer = ask_ram(question, metadatas, history)

    # Update history
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    session["history"] = history[-20:]  # Keep last 10 exchanges

    # Build verse sources
    sources = [
        {"sarga": m["sarga"], "verse": m["verse_number"], "translation": m["translation"]}
        for m in metadatas
    ]

    return jsonify({"answer": answer, "sources": sources})


@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)