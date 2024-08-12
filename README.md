## Generate Indian Recipes using AI
This project generates learns recipes from different Indian cuisines and provides the recipe suggestions based on user's query.  The users can list the available recipe ingredient or they can ask questions about a recipe and the  model can present the related suggestions. 

It uses following technologies and libraries to make it work. This solution implements web API endpoints to provide the interface interact, implement inference and vector store creation to implement RAG technology too.

 - **Langchain**: To implement the work flow for inference and training.
 - **FAISS Vector Store**: To store the documents embedding
	 - It implements **modified pandas dataframe loader** to solve problem where Langchain.DataFrameLoader accepts only one column and by default labeled as "text". [Link](https://github.com/langchain-ai/langchain/issues/12601#issuecomment-2143511307)
- **Models**
	- Embedding Model: Open AI text-embedding-3-large
	- LLM: Ollama3 llama3
- **Web Server**: Gunicorn/uvicorn
- **Web Framework**: FastAPI 
