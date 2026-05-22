import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Step 1 - Load PDF
def load_pdf_files(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

# Step 2 - Split text
def text_split(extracted_data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.split_documents(extracted_data)

# Step 3 - Embeddings
def download_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if __name__ == "__main__":
    # Load and process
    extracted_data = load_pdf_files("data")
    print(f" Loaded {len(extracted_data)} pages")

    text_chunk = text_split(extracted_data)
    print(f" Created {len(text_chunk)} chunks")

    embedding = download_embeddings()
    print(" Embedding model ready")

    # Step 4 - Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "medical-chatbot"

    existing_indexes = [i.name for i in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    print(" Pinecone index ready")

    # Step 5 - Store documents
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunk,
        embedding=embedding,
        index_name=index_name
    )
    print("✅ Documents stored in Pinecone!")