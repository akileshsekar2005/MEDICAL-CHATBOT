import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.helper import download_embeddings
from src.prompt import system_prompt

app = Flask(__name__)
app.secret_key = "medibot-secret-key"

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY     = os.environ.get('GROQ_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_embeddings()

index_name = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

chatModel = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),  # ← memory goes here
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    session.clear()
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg") or request.json.get("msg")
    print("User:", msg)

    # Load chat history from session
    if "chat_history" not in session:
        session["chat_history"] = []

    # Build history as message objects
    chat_history = []
    for h in session["chat_history"]:
        chat_history.append(HumanMessage(content=h["human"]))
        chat_history.append(AIMessage(content=h["ai"]))

    # Run chain with history
    response = rag_chain.invoke({
        "input": msg,
        "chat_history": chat_history
    })

    answer = response["answer"]
    print("Response:", answer)

    # Save to session
    session["chat_history"].append({"human": msg, "ai": answer})
    session["chat_history"] = session["chat_history"][-10:]  # keep last 10
    session.modified = True

    return jsonify({"response": answer})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)