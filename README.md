#  MediBot — AI-Powered Medical Chatbot
 
An intelligent medical chatbot built using **RAG (Retrieval Augmented Generation)**, **LangChain**, **Pinecone**, **HuggingFace Embeddings**, and **Groq LLaMA 3.1** — powered by the Gale Encyclopedia of Medicine.
 
---
 
##  Live Demo
 
> Ask any medical question and get instant, accurate answers from a trusted medical knowledge base.
 
![MediBot Screenshot](screenshots/medibot.png)
 
---
 
##  What This Project Does
 
MediBot is a full-stack AI medical assistant that:
- Loads and processes a medical PDF (Gale Encyclopedia of Medicine — 637 pages)
- Splits it into 5,860+ text chunks
- Converts chunks into vector embeddings using HuggingFace
- Stores embeddings in Pinecone vector database
- Retrieves relevant context for every user question
- Generates accurate answers using Groq LLaMA 3.1
- Remembers conversation history for follow-up questions
- Serves everything through a beautiful Flask web interface
---
 
##  Project Structure
 
```
MEDICAL-CHATBOT/
├── data/
│   └── Medical_book.pdf        # Gale Encyclopedia of Medicine
├── src/
│   ├── __init__.py
│   ├── helper.py               # Embedding download function
│   └── prompt.py               # System prompt for the chatbot
├── templates/
│   └── chat.html               # Frontend chatbot UI
├── static/
│   └── style.css               # Chatbot styles
├── research/
│   └── trials.ipynb            # Jupyter notebook for experiments
├── .env                        # API keys (not uploaded to GitHub)
├── .gitignore
├── app.py                      # Flask application
├── store_index.py              # Script to load PDF and store in Pinecone
├── setup.py
└── requirements.txt
```
 
---
 
##  Tech Stack
 
| Technology | Purpose |
|---|---|
| Python 3.10 | Core programming language |
| Flask | Web framework to serve the chatbot |
| LangChain 0.3.26 | RAG pipeline and chain building |
| HuggingFace Embeddings | Convert text to vectors (all-MiniLM-L6-v2) |
| Pinecone | Vector database to store and retrieve embeddings |
| Groq LLaMA 3.1 | Free LLM for generating answers |
| PyPDF | Load and parse PDF documents |
| python-dotenv | Manage environment variables |
| HTML/CSS/JavaScript | Frontend chatbot interface |
 
---
 
##  Getting Started
 
### 1. Clone the Repository
 
```bash
git clone https://github.com/your-username/MEDICAL-CHATBOT.git
cd MEDICAL-CHATBOT
```
 
### 2. Create and Activate Conda Environment
 
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```
 
### 3. Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Set Up Environment Variables
 
Create a `.env` file in the root directory:
 
```
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
 
Get your free API keys:
- **Pinecone** → https://app.pinecone.io
- **Groq** → https://console.groq.com
### 5. Add Your Medical PDF
 
Place your PDF inside the `data/` folder:
```
data/Medical_book.pdf
```
 
### 6. Store PDF in Pinecone (Run Once)
 
This loads the PDF, creates embeddings, and stores them in Pinecone:
 
```bash
python store_index.py
```
 
### 7. Run the Application
 
```bash
python app.py
```
 
Open your browser and go to:
```
http://localhost:8080
```
 
---
 
##  API Keys Required
 
| Key | Where to Get | Cost |
|---|---|---|
| `PINECONE_API_KEY` | https://app.pinecone.io | Free tier available |
| `GROQ_API_KEY` | https://console.groq.com | Completely free |
 
---
 
##  Requirements
 
```
flask
langchain==0.3.26
langchain-core==0.3.86
langchain-community==0.3.26
langchain-pinecone==0.2.0
langchain-huggingface==0.1.2
langchain-text-splitters==0.3.8
langchain-groq==0.2.5
pinecone
sentence-transformers
pypdf
python-dotenv
```
 
---
 
##  How It Works
 
```
User asks a question
        ↓
Question converted to embedding (HuggingFace)
        ↓
Pinecone searches for similar medical text chunks
        ↓
Top 3 relevant chunks retrieved as context
        ↓
Groq LLaMA 3.1 generates answer using context
        ↓
Answer displayed in chat UI with conversation memory
```
 
---
 
##  Features
 
-  **Medical knowledge base** — 637 pages, 5,860+ chunks from Gale Encyclopedia
-  **Instant responses** — Groq LLaMA 3.1 with sub-2s response time
-  **Conversation memory** — remembers last 10 messages for follow-up questions
-  **Premium dark UI** — glassmorphism design with animations
-  **Mobile responsive** — works on all screen sizes
-  **Privacy first** — zero user data stored
-  **Category filters** — General, Symptoms, Medications, Nutrition, Mental Health, Emergency
-  **Live query counter** — real-time stats bar
---
 
##  Disclaimer
 
MediBot provides general medical information only. It is **not a substitute for professional medical advice**, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.
 
---
 
##  Author
 
**Akilesh**
- GitHub: [@your-username](https://github.com/your-username)
---
 
## License
 
This project is licensed under the MIT License.