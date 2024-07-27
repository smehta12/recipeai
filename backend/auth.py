import os

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from configs import configs
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth(object):
    def create_access_token(self, data):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=configs.auth["access_token_expires_minutes"])
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, os.environ["JWT_SECRET"], algorithm=configs.auth["algorithm"])

        return encoded_jwt


if __name__ == '__main__':
    a = Auth()
    print(a.create_access_token({"user": "shalin"}))
