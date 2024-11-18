from langchain_ibm import WatsonxLLM
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Function to query the WatsonxLLM model
def query_llm(prompt="", vector_db=None):
    """
    Queries the WatsonxLLM model. If a vector database is provided, it performs
    a retrieval augmented generation. Otherwise, it performs a simple inference.

    :param prompt: The input prompt for the model.
    :param vector_db: Optional. The vector database object.
    :return: The response from the model.
    """
    try:
        # Load credentials from .env file
        load_dotenv()

        # Fetch credentials or prompt the user if missing
        WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
        PROJECT_ID = os.getenv("PROJECT_ID")

        if not WATSONX_APIKEY:
            WATSONX_APIKEY = input("WML API key not found in .env. Please enter your WML API key: ").strip()
            print("Reminder: Save your WML API key to the .env file for future use.")
        if not PROJECT_ID:
            PROJECT_ID = input("Project ID not found in .env. Please enter your project ID: ").strip()
            print("Reminder: Save your Project ID to the .env file for future use.")

        # Watsonx credentials
        credentials = {
            "url": "https://eu-gb.ml.cloud.ibm.com",  # Update the URL as required
            "apikey": WATSONX_APIKEY,
            "project_id": PROJECT_ID,
        }

        # WatsonxLLM parameters
        parameters = {
            "max_new_tokens": 100,
            "min_new_tokens": 10,
            "decoding_method": "greedy",
            "temperature": 0.7,
        }

        # Initialize WatsonxLLM
        model = WatsonxLLM(
            model_id="meta-llama/llama-3-1-70b-instruct",
            url=credentials["url"],
            project_id=credentials["project_id"],
            params=parameters,
        )

        # Add system context directly into the user prompt
        contextual_prompt = (
            "You are a highly capable and knowledgeable AI assistant based on the meta-llama/llama-3-70b-instruct model. "
            "Your task is to provide detailed, accurate, and helpful answers to the user's questions. "
            "If required, you will use retrieval-augmented methods to ensure your responses are up-to-date and relevant.\n\n"
            f"User Query: {prompt}"
        )

        if vector_db:
            # Set up retriever and chain for retrieval augmented generation
            retriever = vector_db.as_retriever()
            qa = RetrievalQA.from_chain_type(llm=model, retriever=retriever)
            response = qa.invoke(contextual_prompt)
        else:
            # Simple inference without vector database
            response = model.invoke(contextual_prompt)

        return response
    except Exception as e:
        raise RuntimeError(f"Error during model querying: {e}")
