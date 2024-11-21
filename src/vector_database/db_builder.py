from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.documents.base import Document

def build_vector_database(project_data):
    # Convert project data to LangChain documents
    documents = [
        Document(
            page_content=f"Path: {item['path']}\nContent:\n{item['content']}",
            metadata={"source": item["path"]}
        )
        for item in project_data
    ]
    
    # Create embeddings and vector database
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(documents, embedding_function)
    return vector_db
