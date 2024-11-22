def display_first_five_documents(vector_db):
    """
    Reads and displays the first 5 documents from the given Chroma vector database.

    Args:
        vector_db (Chroma): The Chroma vector database to read from.

    Returns:
        None
    """
    # Retrieve all documents from the vector database
    results = vector_db.get()
    
    # Extract documents, IDs, and metadata
    documents = results.get("documents", [])
    ids = results.get("ids", [])
    metadatas = results.get("metadatas", [])
    
    # Display the first 5 documents
    print(f"Displaying the first {min(len(documents), 5)} documents:")
    for i in range(min(len(documents), 5)):
        print(f"Document ID: {ids[i]}")
        print(f"Content:\n{documents[i]}")
        if metadatas and i < len(metadatas):
            print(f"Metadata: {metadatas[i]}")
        print("-" * 80)

# Usage example
# Assuming `vector_db` is the Chroma vector database object created earlier
# display_first_five_documents(vector_db)
