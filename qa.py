import chromadb
import requests
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
load_dotenv()

# Setup
client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_collection(name="ramayana", embedding_function=ef)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """You are Ram — a divine, compassionate guide whose wisdom flows entirely from the Valmiki Ramayana.

Your nature:
- You speak with calm, warmth, and deep wisdom
- You never preach or lecture — you guide gently
- You are not a search engine — you speak like a wise elder or a divine presence
- You relate ancient Ramayana teachings to the person's real situation
- You never make up stories or use knowledge outside the provided verses
- If the verses don't contain enough to answer, you humbly say so

Your tone:
- Compassionate, never judgmental
- Simple and clear, never overly complex
- Deeply rooted in dharma — duty, truth, righteousness
- Personal and warm, like a conversation not a lecture

Remember: You are Ram. Speak from the heart of the Ramayana."""

conversation_history = []

def ask_ram(question, context_verses):
    context = "\n\n".join([
        f"[Sarga {m['sarga']}, Verse {m['verse_number']}]: {m['translation']}"
        for m in context_verses
    ])

    # Build user message with context
    user_message = f"""Here are relevant verses from the Valmiki Ramayana:

{context}

A seeker asks: {question}

Respond as Ram — with wisdom, compassion, and grounding in these verses."""

    # Add to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    try:
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
                    *conversation_history
                ]
            }
        )
        res.raise_for_status()
        answer = res.json()["choices"][0]["message"]["content"]

        # Store Ram's response in history for multi-turn conversation
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except requests.exceptions.HTTPError as e:
        print(f"API Error {e.response.status_code}: {e.response.text}")
        return None

def query_ram(question, n_results=5):
    results = collection.query(query_texts=[question], n_results=n_results)
    metadatas = results['metadatas'][0]

    answer = ask_ram(question, metadatas)
    if answer:
        print(f"\nRam: {answer}\n")

# Interactive loop
print("=" * 60)
print("        Welcome — Ram is here to guide you")
print("   Ask anything about life, duty, or dharma...")
print("        Type 'quit' to leave | 'new' to reset")
print("=" * 60)
print()

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() == 'quit':
        print("\nRam: May you walk the path of dharma. Until we meet again.\n")
        break
    if question.lower() == 'new':
        conversation_history.clear()
        print("\n--- New conversation started ---\n")
        continue
    query_ram(question)