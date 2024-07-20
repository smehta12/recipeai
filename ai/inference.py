from langchain.chains.retrieval_qa.base import RetrievalQA


class Inference(object):
    def __init__(self, llm, vector_store_obj):
        self.vector_store_obj = vector_store_obj
        self.llm = llm

    def infer(self, prompt):
        retriever = self.vector_store_obj.as_retriever(search_type="similarity_score_threshold",
                                                       search_kwargs={'score_threshold': 0.2})
        # For above steps, create LangChain chain
        qa_stuff = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            verbose=True,
            retriever=retriever,
        )
        response = qa_stuff.run(prompt + " List all of the ingredients, the whole recipe to make, cooking time and total number of servings from the document. Present in good format. DO NOT generate by yourself anything. All the content must be from the documents")

        return response


