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
def query_llm_old(prompt, vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :return: The response from the model.
    """
    try:
        # Specify model parameters
        model_type = "meta-llama/llama-3-70b-instruct"
        max_tokens = 900
        min_tokens = 50
        decoding_method = "greedy"
        temperature = 0.2  # Lowered for factual and concise responses

        # Generate the formatted prompt
        prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"You are a helpful assistant that answers concisely. If unsure, say 'I don't know.'<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )

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

        return response.strip()  # Strip extra spaces or line breaks
    except Exception as e:
        raise RuntimeError(f"Error during model querying: {e}")
def query_llm_new1(prompt, vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :return: The response from the model as a string.
    """
    try:
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
            f"<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )

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
            response = qa.invoke({"query": formatted_prompt})  # Correct key

            # Handle the response format (usually a dictionary)
            if isinstance(response, dict):
                return response.get("result", "").strip()  # Safely get the result key
            elif isinstance(response, str):
                return response.strip()  # Directly strip if it's a string
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")
        else:
            # Simple inference without vector database
            response = model.invoke(formatted_prompt)  # Directly pass the prompt for inference

            # Handle the response format
            if isinstance(response, dict):
                return response.get("result", "").strip()
            elif isinstance(response, str):
                return response.strip()
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")

    except Exception as e:
        raise RuntimeError(f"Error during model querying: {e}")
def query_llm_new2(prompt, vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :return: The response from the model as a string.
    """
    try:
        # Debug: Log the initial prompt and vector_db state
        print(f"Debug: Received prompt: {prompt}")
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
            f"<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )

        # Debug: Log the formatted prompt
        print(f"Debug: Formatted prompt:\n{formatted_prompt}")

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

            # Debug: Log that we're using vector DB
            print("Debug: Querying using vector database...")

            response = qa.invoke({"query": formatted_prompt})  # Correct key

            # Debug: Log the raw response from vector DB
            print(f"Debug: Raw response from vector DB: {response}")

            # Handle the response format
            if isinstance(response, dict):
                result = response.get("result", "").strip()
                # Debug: Log the extracted result
                print(f"Debug: Extracted result from response: {result}")
                return result
            elif isinstance(response, str):
                # Debug: Log the string response
                print(f"Debug: Response as string: {response.strip()}")
                return response.strip()
            else:
                raise ValueError(f"Unexpected response type from vector DB: {type(response)}")
        else:
            # Simple inference without vector database
            print("Debug: Querying without vector database...")
            response = model.invoke(formatted_prompt)

            # Debug: Log the raw response
            print(f"Debug: Raw response from model: {response}")

            # Handle the response format
            if isinstance(response, dict):
                result = response.get("result", "").strip()
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
def query_llm(prompt, vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval-augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The user-provided input for the model.
    :param vector_db: Optional. The vector database object for retrieval-augmented generation.
    :return: The response from the model as a string.
    """
    try:
        # Debug: Log the initial prompt and vector_db state
        print(f"Debug: Received prompt: {prompt}")
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
            f"<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )

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
