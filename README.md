 · MD
# 🏥 MediBot — AI-Powered Medical Chatbot
 
An intelligent medical chatbot built using **RAG (Retrieval Augmented Generation)**, **LangChain**, **Pinecone**, **HuggingFace Embeddings**, and **Groq LLaMA 3.1** — powered by the Gale Encyclopedia of Medicine. Deployed on **AWS EC2** with **Docker**, **Amazon ECR**, and **GitHub Actions CI/CD**.
 
---
 
##  Live Demo
 
**Public URL:** [`http://<your-ec2-public-ip>:8080`](http://13.223.180.212:8080/)
 
---
 
##  What This Project Does
 
MediBot is a full-stack AI medical assistant that:
- Loads and processes a medical PDF (Gale Encyclopedia of Medicine — 637 pages)
- Splits it into 5,860+ text chunks
- Converts chunks into vector embeddings using HuggingFace (all-MiniLM-L6-v2)
- Stores embeddings in Pinecone vector database
- Retrieves relevant context for every user question using similarity search
- Generates accurate answers using Groq LLaMA 3.1
- Remembers conversation history for follow-up questions (last 10 messages)
- Serves everything through a beautiful Flask web interface
- Automatically deploys via GitHub Actions whenever code is pushed
---
 
##  Project Structure
 
```
MEDICAL-CHATBOT/
├── .github/
│   └── workflows/
│       └── main.yaml           # GitHub Actions CI/CD pipeline
├── data/
│   └── Medical_book.pdf        # Gale Encyclopedia of Medicine (637 pages)
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
├── .env                        # API keys (NOT uploaded to GitHub)
├── .gitignore
├── app.py                      # Flask application
├── store_index.py              # Script to load PDF and store in Pinecone
├── Dockerfile                  # Docker container configuration
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
| Docker | Containerize the application |
| Amazon ECR | Store Docker images |
| Amazon EC2 | Host and run the application |
| GitHub Actions | CI/CD pipeline for auto deployment |
| HTML/CSS/JavaScript | Frontend chatbot interface |
 
---
 
##  Implementation — Step by Step
 
### Step 1 — Create Project Structure
 
```bash
mkdir -p src research
touch src/__init__.py src/helper.py src/prompt.py
touch .env setup.py app.py store_index.py requirements.txt
touch research/trials.ipynb
```
 
### Step 2 — Create Conda Environment
 
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```
 
### Step 3 — Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### Step 4 — Set Up Environment Variables
 
Create a `.env` file in the root directory:
 
```
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
 
Get your free API keys:
- **Pinecone** → https://app.pinecone.io (free tier)
- **Groq** → https://console.groq.com (completely free)
### Step 5 — Set Up `src/helper.py`
 
```python
from langchain_huggingface import HuggingFaceEmbeddings
 
def download_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
```
 
### Step 6 — Set Up `src/prompt.py`
 
```python
system_prompt = (
    "You are an expert Medical assistant for question-answering tasks. "
    "Use the following pieces of retrieved context and the chat history "
    "to answer the question. If the context does not have specific information, "
    "use your general medical knowledge to provide a helpful answer. "
    "Always recommend consulting a qualified doctor for diagnosis and treatment. "
    "Keep the answer clear, helpful and concise within 5 sentences."
    "\n\n"
    "{context}"
)
```
 
### Step 7 — Store PDF in Pinecone (Run Once)
 
```bash
python store_index.py
```
 
This loads 637 pages, creates 5,860 chunks, generates embeddings, and stores in Pinecone.
 
### Step 8 — Run Locally
 
```bash
python app.py
```
 
Open browser: `http://localhost:8080`
 
---
 
##  Deployment — AWS EC2 + Docker + GitHub Actions
 
### Step 1 — Create Dockerfile
 
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
```
 
### Step 2 — Push Code to GitHub
 
```bash
git init
git add .
git commit -m "Medical chatbot initial commit"
git branch -M main
git remote add origin https://github.com/your-username/MEDICAL-CHATBOT.git
git push -u origin main
```
 
### Step 3 — Create AWS ECR Repository
 
1. Go to AWS Console → search **ECR**
2. Click **Create repository** → Name: `medibot` → Create
### Step 4 — Launch AWS EC2 Instance
 
1. Go to AWS Console → search **EC2** → **Launch Instance**
2. Settings:
```
Name          → medibot
OS            → Ubuntu 22.04 LTS
Instance type → t2.micro (Free tier eligible)
Key pair      → Create new → medibot-key → Download .pem file
Security group → Allow SSH (22), HTTP (80), Custom TCP (8080)
```
3. Click **Launch Instance**
### Step 5 — Set Up GitHub Secrets
 
Go to GitHub repo → **Settings → Secrets → Actions** → Add:
 
```
AWS_ACCESS_KEY_ID       → your AWS access key
AWS_SECRET_ACCESS_KEY   → your AWS secret key
AWS_REGION              → ap-south-1
AWS_ECR_LOGIN_URI       → your ECR URI
ECR_REPOSITORY_NAME     → medibot
PINECONE_API_KEY        → your pinecone key
GROQ_API_KEY            → your groq key
```
 
### Step 6 — Set Up Self-Hosted Runner on EC2
 
Connect to EC2:
```bash
ssh -i medibot-key.pem ubuntu@<your-ec2-public-ip>
```
 
Install Docker:
```bash
sudo apt-get update -y
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker
```
 
Set up GitHub Actions Runner:
```bash
mkdir actions-runner && cd actions-runner
# Copy commands from GitHub → Settings → Actions → Runners → New self-hosted runner
./config.sh --url https://github.com/your-username/MEDICAL-CHATBOT --token YOUR_TOKEN
```
 
Install as background service:
```bash
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status   # Should show: active (running)
```
 
### Step 7 — GitHub Actions Workflow `.github/workflows/main.yaml`
 
```yaml
name: Deploy MediBot to EC2
 
on:
  push:
    branches: [main]
 
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
 
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
 
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
 
      - name: Build, tag, and push image to ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY_NAME }}
          IMAGE_TAG: latest
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
 
  deploy:
    needs: build-and-push
    runs-on: self-hosted
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
 
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
 
      - name: Pull and run Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY_NAME }}
          IMAGE_TAG: latest
        run: |
          docker stop medibot || true
          docker rm medibot || true
          docker pull $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker run -d \
            --name medibot \
            -p 8080:8080 \
            -e PINECONE_API_KEY=${{ secrets.PINECONE_API_KEY }} \
            -e GROQ_API_KEY=${{ secrets.GROQ_API_KEY }} \
            $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```
 
### Step 8 — Deploy
 
```bash
git add .
git commit -m "Deploy MediBot"
git push origin main
```
 
GitHub Actions automatically builds → pushes to ECR → deploys on EC2.
 
### Step 9 — Access Your App
 
```
http://<your-ec2-public-ip>:8080
```
 
---
 
##  CI/CD Pipeline Flow
 
```
git push to main
      ↓
GitHub Actions triggered
      ↓
Build Docker image (ubuntu-latest runner)
      ↓
Push image to Amazon ECR
      ↓
Self-hosted runner on EC2 pulls new image
      ↓
Old container stopped → New container started
      ↓
App live at http://<ec2-ip>:8080
```
 
---
 
##  How RAG Works
 
```
User asks a question
      ↓
Question → HuggingFace embedding (384 dimensions)
      ↓
Pinecone similarity search → Top 3 relevant chunks
      ↓
Chunks + Chat history → Groq LLaMA 3.1
      ↓
Answer generated and displayed in chat UI
```
 
---
 
##  Features
 
-  Medical knowledge base — 637 pages, 5,860+ chunks from Gale Encyclopedia
-  Instant responses — Groq LLaMA 3.1 with sub-2s response time
-  Conversation memory — remembers last 10 messages for follow-up questions
-  Premium dark UI — glassmorphism design with smooth animations
-  Mobile responsive — works on all screen sizes
-  Privacy first — zero user data stored
-  Category filters — General, Symptoms, Medications, Nutrition, Mental Health, Emergency
-  Live query counter — real-time stats bar
-  Dockerized — consistent deployment everywhere
-  Auto CI/CD — deploy on every git push
- ☁️ Hosted on AWS EC2 — accessible worldwide 24/7
---
 
##  Disclaimer
 
MediBot provides general medical information only. It is **not a substitute for professional medical advice**, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.
 
---
 
##  Author
 
**Akilesh**
- GitHub: [@akileshsekar2005](https://github.com/akileshsekar2005)
- Email: akileshsekar2005@gmail.com
---
 
##  License
 
This project is licensed under the MIT License.
 
