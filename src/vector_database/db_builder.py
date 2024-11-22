from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.documents.base import Document

def build_vector_database(project_data, persist_directory=None):
    """
    Builds a vector database from project data.

    Args:
        project_data: The data to build the database from.
        persist_directory: (Optional) The directory to persist the database to.
    
    Returns:
        Chroma: The Chroma vector database object.
    """
    # Convert project data to LangChain documents
    documents = [
        Document(
            page_content=f"Path: {item['path']}\nContent:\n{item['content']}",
            metadata={"source": item["path"]}
        )
        for item in project_data
    ]
    
    # Create embeddings and vector database
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if persist_directory:
        # Create or load the persistent Chroma vector database
        vector_db = Chroma.from_documents(
            documents=documents,
            embedding=embedding,  # Use 'embedding' instead of 'embedding_function'
            persist_directory=persist_directory
        )
        vector_db.persist()
    else:
        # Create a transient Chroma vector database
        vector_db = Chroma.from_documents(documents, embedding=embedding)  # Use 'embedding' instead of 'embedding_function'
    
    return vector_db





def load_vector_database(persist_directory): 
    """
    Loads a persisted Chroma vector database from disk.

    Args:
        persist_directory: The directory the database is persisted in. 
                           This argument is required.

    Returns:
        Chroma: The Chroma vector database object.

    Raises:
        ValueError: If persist_directory is not provided.
    """
    if not persist_directory:
        raise ValueError("persist_directory must be provided to load the database.")

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(
        embedding_function=embedding_function, 
        persist_directory=persist_directory
    )
    return vector_db