from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np  # Optional, for numerical operations on embeddings (if needed)
import pandas as pd
# Provide the path relative to the dir in which the script is running
file_path = "../data/output.pkl"
# Load the dataframe from the pickle file
df = pd.read_pickle(file_path)

# Create an empty list to store the vectors
vectors_database = []

# Get the text content from the "Content" column
text_content = df["Content"].tolist()
text_content
# Choose an appropriate model:
model_name = "sentence-transformers/all-mpnet-base-v2"  # Replace with your desired model if needed
# Set device (CPU or GPU) based on your hardware and performance requirements:
model_kwargs = {'device': 'cpu'}  # Change to 'cuda' for GPU usage (if available)
# Encoding options (normalization is often recommended):
encode_kwargs = {'normalize_embeddings': True}  # Experiment with normalization

# Initialize the embedding model:
hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# Create an empty list to store the embeddings:
embeddings_list = []

# Process your text content (replace with your actual text data):
text_content = ["This is the first sentence.", "This is the second sentence."]

for text in text_content:
    # Preprocess text if necessary (e.g., tokenization, cleaning)
    # processed_text = preprocess_text(text)  # Implement your preprocessing function (optional)

    # **Corrected embedding generation:**
    embedding = hf.embed_query(text)  # Use embed_query for single text

    # Append the embedding vector directly (no need to extract):
    embeddings_list.append(embedding)

# Now you have a list of embeddings (each embedding is a list of floats)
# Use these embeddings for your further analysis or tasks
print(embeddings_list)