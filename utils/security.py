from passlib.context import CryptContext #Passlib is a Python library used for secure password hashing.
from jose import jwt #python-jose is a library used to create and verify JWT (JSON Web Tokens).
from datetime import datetime, timedelta, UTC

import os
from dotenv import load_dotenv

load_dotenv()

# bcrypt is the hashing algorithm
pwd_context = CryptContext(
    schemes=["bcrypt"], #Even the same password produces different hashes using bcrypt
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password, #what the user just typed
        hashed_password #what is stored in PostgreSQL.
    )
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )