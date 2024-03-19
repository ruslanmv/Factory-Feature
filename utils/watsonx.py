# For reading credentials from the .env file
import os
from dotenv import load_dotenv
import pandas as pd

from langchain.document_loaders import PyPDFLoader, DataFrameLoader
from langchain.chains import RetrievalQA
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# WML python SDK
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM

# Load API credentials from .env file
load_dotenv()
try:
    API_KEY = os.environ.get("API_KEY")
    project_id = os.environ.get("PROJECT_ID")
except KeyError:
    API_KEY = input("Please enter your WML api key (hit enter): ")
    project_id = input("Please enter your project_id (hit enter): ")

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": API_KEY
}


def get_model(model_type, max_tokens, min_tokens, decoding, temperature):

    generate_params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.TEMPERATURE: temperature
    }

    model = Model(
        model_id=model_type,
        params=generate_params,
        credentials=credentials,
        project_id=project_id
    )

    return model


def get_lang_chain_model(model_type, max_tokens, min_tokens, decoding, temperature):

    base_model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)
    langchain_model = WatsonxLLM(model=base_model)

    return langchain_model


def main():
    # Test answering questions based on the provided dataframe
    question = "What are the limitations of generative AI models?"
    
    # Provide the path relative to the dir in which the script is running
    file_path = "./workspace/output.pkl"

    answer_questions_from_dataframe(file_path, question)


def answer_questions_from_dataframe(file_path, question):
    # Specify model parameters
    model_type = "meta-llama/llama-2-70b-chat"
    max_tokens = 300
    min_tokens = 100
    decoding = DecodingMethods.GREEDY
    temperature = 0.7

    # Get the watsonx model that can be used with LangChain
    model = get_lang_chain_model(model_type, max_tokens, min_tokens, decoding, temperature)

    # Load the dataframe from the pickle file
    df = pd.read_pickle(file_path)

    # Create an empty list to store the vectors
    vectors_database = []

    # Get the text content from the "Content" column
    text_content = df["Content"].tolist()

    # Use HuggingFaceEmbeddings to generate vectors for each text
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    for text in text_content:
        vector = embeddings.encode_batch([text])
        vectors_database.append(vector[0])

    # Print or save the updated vector database
    print(vectors_database)  # Replace with appropriate method for saving the database

    loaders = [DataFrameLoader(df)]

    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        ),
        text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    ).from_loaders(loaders)

    chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=index.vectorstore.as_retriever(),
        input_key="question"
    )

    response_text = chain.run(question)

    print("--------------------------------- Generated response -----------------------------------")
    print(response_text)
    print("*********************************************************************************************")

    return response_text

# Invoke the main function
if __name__ == "__main__":
    main()
