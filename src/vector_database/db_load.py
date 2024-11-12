from chromadb import PersistentClient
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import torch
# Load the Chroma database
def load_vector_db(collection_name, persist_directory):
    """
    Load an existing Chroma vector database collection.

    Args:
        collection_name (str): Name of the collection.
        persist_directory (str): Path to the persistent directory.

    Returns:
        Chroma: Loaded vector database.
    """
    # Initialize PersistentClient
    chroma_client = PersistentClient(path=persist_directory)

    # Check if the collection exists
    if collection_name not in [col.name for col in chroma_client.list_collections()]:
        raise ValueError(f"Collection '{collection_name}' does not exist. Make sure it is created.")

    # Get the collection
    collection = chroma_client.get_collection(name=collection_name)

    # Use the same embedding model used for storing data
    model_name = "sentence-transformers/all-mpnet-base-v2"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}

    # Initialize embedding function
    hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    # Return Chroma vector database
    return Chroma(collection_name=collection_name, embedding_function=hf, client=chroma_client)



