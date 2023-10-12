import pickle

async def create_vector_search(config):
    with open(config["VECTOR_SAVING_DIR"], 'rb') as f:
        serialized_vectors = f.read()
        vector_search = pickle.loads(serialized_vectors)
    return vector_search