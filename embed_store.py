import json
import chromadb
from chromadb.utils import embedding_functions

# Load data
print("Loading data...")
with open("ramayana_data_test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten verses
print("Flattening verses...")
verses = []
for kanda_key, sargas in data['kandas'].items():
    for sarga_num, verse_list in sargas.items():
        for verse in verse_list:
            verses.append({
                "id": f"{kanda_key}_{sarga_num}_{verse['verse_number']}",
                "text": f"{verse['translation']} {verse.get('meanings', '')}",
                "kanda": kanda_key,
                "sarga": sarga_num,
                "verse_number": str(verse['verse_number']),
                "translation": verse['translation'],
                "sanskrit": verse['sanskrit'],
            })

print(f"Total verses: {len(verses)}")

# Setup ChromaDB
print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="ramayana",
    embedding_function=ef
)

# Store in batches of 100
print("Embedding and storing...")
batch_size = 100
for i in range(0, len(verses), batch_size):
    batch = verses[i:i+batch_size]
    collection.add(
        ids=[v["id"] for v in batch],
        documents=[v["text"] for v in batch],
        metadatas=[{
            "kanda": v["kanda"],
            "sarga": v["sarga"],
            "verse_number": v["verse_number"],
            "translation": v["translation"],
            "sanskrit": v["sanskrit"],
        } for v in batch]
    )
    print(f"  Stored {min(i+batch_size, len(verses))}/{len(verses)} verses...")

print("✓ Done! All verses embedded and stored in ChromaDB.")