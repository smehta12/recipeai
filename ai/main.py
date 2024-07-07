from vector_store import VectorStore


def generate_vector_store():
    vs = VectorStore()
    vs.create_and_save_vector_store()


if __name__ == '__main__':
    generate_vector_store()