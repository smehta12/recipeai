from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from configs import configs

from ai.vector_store import VectorStore
from ai.inference import Inference


def get_vector_store(create_store=False):
    embedding_model = HuggingFaceEmbeddings(model_name=configs.embedding_model,
                                            model_kwargs=dict(trust_remote_code=True))
    vs = VectorStore(FAISS, embedding_model)
    if create_store:
        vs.create_and_save_vector_store()
    return vs


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
    pr = f"Show me one dhokla recipe"
    print(inference(get_vector_store(), pr))
