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

def generate_prompt(user_input, grounding=None, system_message="You are a helpful assistant that avoids causing harm. When you do not know the answer to a question, you say 'I don't know'."):
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

# Common function to get the language model
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

# Answer questions using a vector database
def answer_questions_from_dataframe(question, collection_name, persist_directory="./notebooks/chroma_db"):
    """
    Answers a question using a LangChain model and retrieves relevant documents from a Chroma collection.
    """
    # Specify model parameters
    model_type = "meta-llama/llama-3-1-70b-instruct"
    max_tokens = 300
    min_tokens = 100
    decoding_method = "greedy"
    temperature = 0.7

    # Initialize the WatsonxLLM model
    model = get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature)

    # Use the same embedding model as in create_embeddings_and_store for consistency
    model_name = "sentence-transformers/all-mpnet-base-v2"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}

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

    # Create a retriever from the vectorstore
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Build the RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
    )

    # Run the chain with the question
    response_text = chain.invoke({"query": question})  # Correct key

    print("--------------------------------- Generated response -----------------------------------")
    print(response_text)
    print("*********************************************************************************************")

    return response_text

# Query the LLM directly

def query_llm(user_input, vector_db=None, grounding=None,system_message=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param user_input: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :param grounding: Optional. Contextual grounding information to improve the response.
    :param system_message: Optional.The system-level instruction for the assistant.    
    :return: The response from the model as a string.
    """
    try:
        # Debug: Log the initial prompt and vector_db state
        print(f"Debug: Received prompt: {user_input}")
        print(f"Debug: Vector DB provided: {bool(vector_db)}")

        # Specify model parameters
        model_type = "meta-llama/llama-3-70b-instruct"
        max_tokens = 900
        min_tokens = 50
        decoding_method = "greedy"
        temperature = 0.2  # Lowered for factual and concise responses

        # Generate the formatted prompt
        formatted_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"You are a helpful assistant that answers concisely. If unsure, say 'I don't know.'<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )

        # Generate the formatted prompt
        formatted_prompt = generate_prompt(user_input, grounding,system_message)        

        # Debug: Log the formatted prompt
        print(f"Debug: Formatted prompt:\n{formatted_prompt}")

        # Initialize the WatsonxLLM model
        model = get_lang_chain_model(model_type, max_tokens, min_tokens, decoding_method, temperature)

        if vector_db:
            # Retrieval-augmented generation
            retriever = vector_db.as_retriever(search_kwargs={"k": 5})
            qa = RetrievalQA.from_chain_type(
                llm=model,
                chain_type="stuff",
                retriever=retriever,
            )

            # Debug: Log that we're using vector DB
            print("Debug: Querying using vector database...")
            try:
                response = qa.invoke({"query": formatted_prompt})
                # Debug: Log the raw response from vector DB
                print(f"Debug: Raw response from vector DB: {response}")
                #return response
                # Extract only the LLM result
                if isinstance(response, dict) and "result" in response:
                    result = response["result"].strip()
                    # Debug: Log the extracted result
                    print(f"Debug: Extracted result: {result}")
                    return result
                else:
                    raise ValueError(f"Unexpected response format: {response}")
            except:
                raise ValueError(f"Unexpected response type from vector DB: {response}")
        else:
            # Simple inference without vector database
            print("Debug: Querying without vector database...")
            response = model.invoke(formatted_prompt)

            # Debug: Log the raw response
            print(f"Debug: Raw response from model: {response}")

            # Handle the response format
            if isinstance(response, dict):
                result = response.get("result") or response.get("text", "").strip()
                if not result:
                    raise ValueError("No 'result' or 'text' key found in response.")
                # Debug: Log the extracted result
                print(f"Debug: Extracted result from response: {result}")
                return result
            elif isinstance(response, str):
                # Debug: Log the string response
                print(f"Debug: Response as string: {response.strip()}")
                return response.strip()
            else:
                raise ValueError(f"Unexpected response type from model: {type(response)}")
    except Exception as e:
        # Debug: Log the exception
        print(f"Debug: Exception occurred: {e}")
        raise RuntimeError(f"Error during model querying: {e}")
