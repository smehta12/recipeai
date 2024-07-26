from langchain_community.vectorstores import FAISS
from ai.vector_store import get_vector_store
from ai.inference import Inference

def inference(vs_obj, prompt):
    """

    :param prompt:
    :param vs_obj: Vector Store object of VectorStore
    :return:
    """
    from langchain_community.llms import Ollama
    llm = Ollama(model="llama3", temperature=0.5)
    i = Inference(llm, vs_obj.get_saved_vector_store())
    return i.infer(prompt)


if __name__ == '__main__':
    get_vector_store(FAISS, create_store=True)
    pr = f"Show me one dhokla recipe"
    print(inference(get_vector_store(FAISS), pr))
    pass
