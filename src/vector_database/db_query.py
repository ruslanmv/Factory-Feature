def query_vector_database(vector_db, query, top_k=5):
    """
    Queries the vector database for relevant documents.

    Args:
        vector_db: The vector database instance.
        query: The search query.
        top_k: Number of top documents to retrieve.

    Returns:
        List of relevant documents.
    """
    retriever = vector_db.as_retriever(search_kwargs={"k": top_k})
    return retriever.get_relevant_documents(query)
