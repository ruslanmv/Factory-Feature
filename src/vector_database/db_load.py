from chromadb import PersistentClient
from chromadb.config import Settings
from langchain.vectorstores import Chroma
# Load the Chroma database
# vector_database/db_load.py
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb import PersistentClient
import torch
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def load_vector_db_by_collection(collection_name, persist_directory="./chroma_db"):
    """
    Loads a Chroma vector database.

    :param collection_name: The name of the collection to load.
    :param persist_directory: The directory where the database is stored.
    :return: The Chroma collection object.
    """
    # Use the same embedding model as in create_embeddings_and_store for consistency
    model_name = "sentence-transformers/all-mpnet-base-v2"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings':  True}

    # Initialize the embedding model
    hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    # Initialize Chroma Persistent Client
    chroma_client = PersistentClient(path=persist_directory)

    # Ensure the collection exists
    if collection_name not in [col.name for col in chroma_client.list_collections()]:
        raise ValueError(f"Collection '{collection_name}' does not exist. Make sure it is created.")
    collection = chroma_client.get_collection(name=collection_name)

    # Use Chroma vectorstore with the given collection
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=hf,
        client=chroma_client,
    )

    return vector_store

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