import logging
import os

import uvicorn
import gc
import jwt

from pydantic import BaseModel
from fastapi import FastAPI, Response, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ai.vector_store import get_vector_store
from ai.inference import Inference
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

from backend.auth import Auth
from configs import configs

app = FastAPI()


@app.get("/")
def home():
    print("Welcome to Indian AI generated Recipes")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential. Please re-login",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=configs.auth["algorithm"])
        username = payload.get("user")

        if not username or username not in configs.auth["allowed_users"]:
            raise credential_exception

        return {'username': username}
    except jwt.exceptions.ExpiredSignatureError:
        raise credential_exception
    except:
        raise


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


@app.post("/token", tags=["Login"], response_model=Token)
async def login_for_acess_token(form_data: OAuth2PasswordRequestForm = Depends()):
    allowed_user_names = configs.auth["allowed_users"]
    password = os.environ["PROJ_LOGIN_PASSWORD"]  # indian recipes from generative ai

    try:
        form_user = form_data.username
        if form_user.lower() not in allowed_user_names or form_data.password != password:
            raise HTTPException(status_code=401, detail=f"Invalid user name {form_user} or password")

        a = Auth()
        data = {"user": form_data.username.lower()}
        access_token = a.create_access_token(data)

        logging.info(f"User {form_user} logged in")

        return {"access_token": access_token, "token_type": "Bearer"}
    except:
        logging.exception(f"Couldn't login with uname:{form_data.username}, and password: {form_data.password}")
        raise


@app.get("/user/me", tags=['Login'], response_model=TokenData)
async def read_user_me(current_user=Depends(get_current_user)):
    return current_user


@app.post("/search", response_model=str)
async def search(prompt: str, current_user: TokenData = Depends(get_current_user)):
    logging.info(f"User {current_user} tried.")
    llm = Ollama(model="llama3", temperature=0.5, cache=False)
    vs = get_vector_store(FAISS, create_store=False).get_saved_vector_store()
    i = Inference(llm, vs)
    ans = i.infer(prompt)
    del llm
    del i
    gc.collect()
    return ans


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8889, reload=True, log_level='info')
