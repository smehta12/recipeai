import uvicorn
import gc
import torch

from fastapi import FastAPI, Response, Request
from ai.vector_store import get_vector_store
from ai.inference import Inference
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

app = FastAPI()

@app.get("/")
def home():
    print("Welcome to Indian AI generated Recipes")

@app.post("/search")
async def search(prompt: str):
    llm = Ollama(model="llama3", temperature=0.5, cache=False)
    vs = get_vector_store(FAISS, create_store=False).get_saved_vector_store()
    i = Inference(llm, vs)
    ans = i.infer(prompt)
    del llm
    del i
    # torch.cuda.empty_cache()
    # torch.cuda.ipc_collect()
    gc.collect()
    return ans

# @app.on_event("shutdown")
# def shutdown_event():
#     print("Shutting down...")
#     torch.cuda.empty_cache()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8889, reload=True, log_level='info')
