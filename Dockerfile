FROM python:3.11.8

LABEL maintainer="shalinmehta85@gmail.com"

RUN apt-get update && apt-get install git -y && apt-get install curl -y

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY . /app

RUN pip install setuptools==68.2.2
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
RUN pip install -e .

# RUN ollama run llama3 &
RUN ollama serve & sleep 5 && ollama run llama3

CMD ["uvicorn", "--app-dir=./backend", "main:app", "--host", "0.0.0.0", "--port", "8888", "--log-level", "debug"]
#CMD ["gunicorn", "--workers", "4", "worker-class", "uvicorn.workers.UvicornWorker", "--chdir=./backend", "main:app", "--bind=0.0.0.0:8888", "--log-level", "debug"]