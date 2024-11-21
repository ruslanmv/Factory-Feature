from chromadb import PersistentClient
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import torch
# Load the Chroma database
# vector_database/db_load.py
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb import PersistentClient
import torch

def load_vector_db(collection_name, persist_directory="./chroma_db"):
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

