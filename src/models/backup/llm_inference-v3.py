# llm_inference.py
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ibm import WatsonxLLM
from chromadb import PersistentClient
import torch

# Load credentials from .env file
load_dotenv()
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
PROJECT_ID = os.getenv("PROJECT_ID")

if not WATSONX_APIKEY or not PROJECT_ID:
    raise ValueError("API key or Project ID is missing. Please check your .env file.")

def get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature):
    """
    Initializes and returns a WatsonxLLM instance with the specified parameters.
    """
    return WatsonxLLM(
        model_id=model_type,
        url="https://eu-gb.ml.cloud.ibm.com",
        project_id=PROJECT_ID,
        params={
            "max_new_tokens": max_tokens,
            "min_new_tokens": min_tokens,
            "decoding_method": decoding_method,
            "temperature": temperature,
        },
    )

def query_llm(prompt="", vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The input prompt for the model.
    :param vector_db: Optional. The vector database object.
    :return: The response from the model.
    """
    try:
        # Specify model parameters
        model_type = "meta-llama/llama-3-1-70b-instruct"
        max_tokens = 100
        min_tokens = 200
        decoding_method = "greedy"
        temperature = 0.7

        # Initialize the WatsonxLLM model
        model = get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature)

        if vector_db:
            # Retrieval augmented generation
            retriever = vector_db.as_retriever(search_kwargs={"k": 5})
            qa = RetrievalQA.from_chain_type(
                llm=model,
                chain_type="stuff",
                retriever=retriever,
            )
            response = qa.invoke({"query": prompt})  # Use 'query' as the input key
        else:
            # Simple inference without vector database
            response = model.invoke(prompt)  # Directly pass the prompt for inference

        return response
    except Exception as e:
        raise RuntimeError(f"Error during model querying: {e}")