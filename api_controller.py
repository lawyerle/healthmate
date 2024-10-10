from fastapi import FastAPI
from main import chat_with_user, make_chain, init_api, chain

app = FastAPI()

def prepare():
    init_api()
    make_chain()

@app.get("/hello")
def hello():
    return {'message': "Hello"}

@app.get('/chat/{question}')
def chat(question: str):
    message = chat_with_user(question)

    return {'message': message}

prepare()
