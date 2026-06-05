# 🙏 Ram — Divine Wisdom Guide

A **RAG-based (Retrieval-Augmented Generation) conversational AI** that channels wisdom from the **Valmiki Ramayana** to answer your life questions with compassion and depth.

> **Ram** is not just a chatbot—it's a thoughtful guide who speaks from the heart of India's oldest epic, offering timeless wisdom rooted in dharma, duty, courage, and righteousness.

---

## 🌟 What is Ram-ai?

**Ram** is an AI-powered wisdom guide that:
- 📚 **Grounds responses** exclusively in verses from the Valmiki Ramayana
- 🔍 **Retrieves relevant verses** using semantic search (ChromaDB + embeddings)
- 💬 **Generates thoughtful answers** using the Llama 3.3 70B model (via Groq API)
- 🎭 **Speaks like Ram**—simple, warm, and wise, never preachy or overly philosophical
- 📖 **Shows sources**—every answer includes the exact verses it's based on

Perfect for seekers exploring questions about **life, duty, loss, courage, relationships, ethics, and the path of righteousness**.

---

## 🏗️ Architecture

```
User Question
     ↓
[Semantic Search] ← ChromaDB (Ramayana verses + embeddings)
     ↓
[Context Verses Retrieved] ← 5 most relevant verses
     ↓
[LLM Prompt] → Groq API (Llama 3.3 70B)
     ↓
[Ram's Answer] → Displayed with verse sources
```

### Tech Stack
- **Backend**: Python + Flask
- **Vector Database**: ChromaDB (persistent, local storage)
- **Embeddings**: Default embedding function (all-MiniLM-L6-v2)
- **LLM**: Llama 3.3 70B (via Groq API)
- **Frontend**: HTML5 + Vanilla JavaScript
- **Web Scraping**: BeautifulSoup (for Ramayana data extraction)

---

## 📁 Project Structure

```
Ram-ai/
├── app.py                    # Flask web server & main application
├── embed_store.py            # Embeds verses & stores in ChromaDB
├── qa.py                     # CLI interface for Ram (interactive mode)
├── ramayana_scraper_test.py  # Web scraper for Ramayana verses
├── templates/
│   └── index.html            # Beautiful frontend UI
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

### Key Files Explained

#### **app.py** — The Web Server
- **Route `/`**: Serves the beautiful index.html interface
- **Route `/ask`**: Accepts user questions (POST), retrieves verse context, calls LLM, returns answer + sources
- **Route `/reset`**: Clears conversation history
- Manages conversation history (last 10 exchanges) for context-aware responses

#### **embed_store.py** — Vector Database Setup
- Loads Ramayana verses from `ramayana_data_test.json`
- Converts each verse into embeddings
- Stores embeddings + metadata in ChromaDB (persistent database)
- **Run once** to initialize the vector database

#### **qa.py** — CLI Interactive Mode
- Simple command-line interface for talking to Ram
- Maintains multi-turn conversation history
- Type `quit` to exit, `new` to start fresh conversation
- Perfect for quick testing without opening the web UI

#### **ramayana_scraper_test.py** — Web Scraper
- Scrapes Ramayana verses from [valmikiramayan.net](https://valmikiramayan.net/)
- Extracts Sanskrit text, translations, meanings, and commentary
- Saves as JSON with structured metadata (Kanda, Sarga, Verse number)
- Currently configured for Bala Kanda (test version)

#### **templates/index.html** — Frontend UI
- **Beautiful, sacred aesthetic**: Gold + dark theme inspired by temple design
- Real-time chat interface with message bubbles
- "View Source Verses" button to see which Ramayana verses informed each answer
- Typing indicator while Ram thinks
- Auto-resizing textarea for comfortable input
- "New Conversation" button to reset history
- Fully responsive design

---

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/srilalita-05/Ram-ai.git
cd Ram-ai
```

### 2. **Set Up Python Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install flask chromadb requests python-dotenv beautifulsoup4
```

### 4. **Set Up Environment Variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Get your Groq API Key**:
1. Sign up at [groq.com](https://groq.com)
2. Navigate to API keys section
3. Create a new key and copy it
4. Paste into `.env` file

### 5. **Prepare Ramayana Data**
You need a `ramayana_data_test.json` file with verse data. Two options:

**Option A: Use the Scraper** (Generate from web)
```bash
python ramayana_scraper_test.py
```
This will create `ramayana_data_test.json` with Bala Kanda verses.

**Option B: Provide Your Own**
Create `ramayana_data_test.json` with this structure:
```json
{
  "metadata": { "source": "...", "total_kandas": 1, "kandas": [] },
  "kandas": {
    "baala": {
      "1": [
        {
          "verse_number": 1,
          "sanskrit": "...",
          "translation": "...",
          "meanings": "...",
          "commentary": "..."
        }
      ]
    }
  }
}
```

### 6. **Embed Verses into ChromaDB**
```bash
python embed_store.py
```
This creates a `chroma_db/` folder with embedded verses.

### 7. **Run the Flask App**
```bash
python app.py
```
Open your browser to `http://localhost:5000`

---

## 💬 How to Use

### Web Interface
1. Open `http://localhost:5000`
2. Type your question: *"What should I do when I feel lost?"*
3. Press **Enter** or click **Ask**
4. Ram responds with wisdom rooted in Ramayana verses
5. Click **View Source Verses** to see which verses informed the answer
6. Ask follow-up questions—Ram remembers context
7. Click **New Conversation** to reset history

### CLI Interface
```bash
python qa.py
```
Then type your questions directly:
```
You: What does the Ramayana teach about duty?
Ram: [Answer grounded in verses...]

You: Tell me more about that.
Ram: [Context-aware follow-up...]

You: quit
Ram: May you walk the path of dharma. Until we meet again.
```

---

## 🔑 Key Features

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Finds verses relevant to your question's meaning, not just keywords |
| **Grounded Responses** | All answers are based exclusively on Ramayana verses |
| **Multi-turn Dialogue** | Remembers conversation context (last 10 exchanges) |
| **Source Attribution** | Shows exact Sarga & Verse for every answer |
| **Sacred Design** | Frontend uses gold+dark temple aesthetic |
| **Simple Language** | Ram speaks like a wise friend, not a scholar |
| **Offline-First** | Verses stored locally in ChromaDB (no daily API calls) |

---

## ⚙️ Configuration

### Adjust LLM Parameters (in `app.py` & `qa.py`)
```python
SYSTEM_PROMPT = """Your system instruction here"""
# Change to customize Ram's personality
```

### Adjust Semantic Search (in `app.py`)
```python
results = collection.query(query_texts=[question], n_results=5)
# Change n_results=5 to get more/fewer context verses
```

### Adjust Request Delay (in `ramayana_scraper_test.py`)
```python
REQUEST_DELAY = 1.5  # Seconds between requests (be respectful to servers!)
```

---

## 📊 Data Flow

```
Ramayana Verses (valmikiramayan.net)
         ↓
    [Scraper] → ramayana_data_test.json
         ↓
    [Embedder] → ChromaDB (vectors + metadata)
         ↓
    [User Question] ← [Web UI / CLI]
         ↓
    [Semantic Search] → 5 relevant verses
         ↓
    [LLM Prompt] + [System Prompt] + [History]
         ↓
    [Ram's Response] → Displayed to user
```

---

## 🔧 Troubleshooting

### ❌ "ChromaDB not found"
```bash
python embed_store.py  # Run embedder first
```

### ❌ "GROQ_API_KEY error"
- Check `.env` file exists in root directory
- Verify API key is correct (no spaces/typos)
- Test key at [groq.com](https://groq.com)

### ❌ "No verses found" from scraper
- Website structure may have changed
- Check `valmikiramayan.net` manually
- Verify internet connection

### ❌ Responses are not grounded in Ramayana
- Increase `n_results` in search to get more context
- Check that `ramayana_data_test.json` is properly formatted
- Ensure embeddings were created: `python embed_store.py`

---

## 📖 Philosophy: Why Ram-ai?

The Ramayana is humanity's oldest epic—14,000 verses exploring duty, sacrifice, justice, courage, and dharma. Its wisdom transcends centuries and cultures.

**Ram-ai** bridges ancient wisdom and modern AI:
- ✨ **No hallucinations**: Responses rooted in actual text, not imagination
- 🧠 **Context-aware**: Semantic search finds verses by *meaning*, not keywords
- 💬 **Conversational**: Multi-turn history lets Ram understand deeper context
- 🏛️ **Reverent**: Treats sacred text with respect, never as just data

---

## 🤝 Contributing

Ideas for improvements?
- Add more Kandas (currently Bala Kanda only)
- Improve scraper for full Ramayana coverage
- Add support for multiple Indian languages
- Create conversation examples/templates
- Improve frontend accessibility

---

## 📝 License

This project is open source. Please respect the sacredness of the Valmiki Ramayana when using this tool.

---

## 🙏 Acknowledgments

- **Valmiki Ramayana** — The eternal source of wisdom
- **Groq** — For fast, accessible LLM inference
- **ChromaDB** — For elegant vector database capabilities
- **All seekers** — Who ask genuine questions about life and dharma

---

## 📞 Questions?

If you encounter issues or have suggestions:
1. Check the **Troubleshooting** section above
2. Review `.env` and configuration files
3. Ensure all dependencies are installed
4. Verify `ramayana_data_test.json` exists

---

**Om Namah Shivaya** 🙏

> *"The greatest knowledge is the knowledge of oneself. The greatest wisdom is the wisdom to serve others."* — The Ramayana
