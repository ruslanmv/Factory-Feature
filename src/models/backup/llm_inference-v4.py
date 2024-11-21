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

def generate_prompt(user_input, grounding=None, system_message="You are a helpful assistant. Respond to the user query concisely and accurately. If you don't know, say 'I don't know'."):
    """
    Generates a formatted prompt using the specified input, grounding, and system message.

    :param user_input: The user-provided input question or statement.
    :param grounding: Optional grounding information to provide additional context.
    :param system_message: The system-level instruction for the assistant.
    :return: A formatted string prompt.
    """
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
    )
    if grounding:
        prompt += f"{grounding}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
    prompt += f"{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    return prompt

def get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature, repetition_penalty):
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
            "repetition_penalty": repetition_penalty,
        },
    )

def query_llm(user_input, vector_db=None, grounding=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param user_input: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :param grounding: Optional. Contextual grounding information to improve the response.
    :return: The response from the model.
    """
    try:
        # Specify model parameters
        model_type = "meta-llama/llama-3-70b-instruct"
        max_tokens = 10
        min_tokens = 5
        decoding_method = "greedy"
        temperature = 0.2  # Lowered for factual and concise responses
        repetition_penalty = 1.2  # Penalize repeated patterns

        system_message='''
        You are a helpful assistant. Respond to the user query concisely and accurately. If you don't know, say 'I don't know'.
        Please use concrete answers.
        '''
        # Generate the formatted prompt
        prompt = generate_prompt(user_input, grounding,system_message)
        print("Prompt Used:", prompt)
        # Initialize the WatsonxLLM model
        model = get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature, repetition_penalty)

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

        return response.strip()  # Strip extra spaces or line breaks
    except Exception as e:
        raise RuntimeError(f"Error during model querying: {e}")
