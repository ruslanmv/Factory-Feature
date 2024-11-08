from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM

def query_llm(vector_db, prompt):
    model = WatsonxLLM(model_id="meta-llama/llama-2-70b-chat")
    retriever = vector_db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=model, retriever=retriever)
    response = qa.run(prompt)
    return response
