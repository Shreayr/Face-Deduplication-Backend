from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session #Imports the SQLAlchemy session.
from fastapi import Depends, HTTPException #Allows FastAPI to inject dependencies automatically.

from database import get_db #get_db() which creates and closes database sessions.
from database_models import User #Imports the User table.
from models import UserCreate, UserResponse,UserLogin #Imports the Pydantic models.

#Imports security functions.
from utils.security import verify_password #Hash password 
from utils.security import create_access_token #Check login password
from utils.security import hash_password #Create JWT

from fastapi import FastAPI #Imports FastAPI.

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from utils.security import SECRET_KEY, ALGORITHM

from database import engine
from database import Base

from fastapi import UploadFile, File
import shutil
import os

from database_models import UploadedImage
import uuid
from fastapi.staticfiles import StaticFiles
from typing import List

import database_models

app = FastAPI() #Anything inside the uploads folder can be accessed through /uploads.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ #Only these websites are allowed to call your backend.
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True, #Allows cookies and authentication.
    allow_methods=["*"], #Allow all HTTP methods.GET POST PUT DELETE
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine) #Reads database_models.py and creates tables if they don't exist.

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user

@app.get("/")
def home():
    return {"message": "Face Deduplication Backend Running"}

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check whether the email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create a new User object
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role="client"
    )

    # Save into database
    db.add(new_user) #Adds to session.Not yet stored.

    # Commit changes
    db.commit() #Actually stores it in PostgreSQL.

    # Refresh to get generated id
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": db_user.email} #sub means Subject.It identifies the owner of the token.
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/upload-image")
def upload_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    # Save path
    unique_filename = f"{uuid.uuid4()}_{image.filename}" #This avoids filename collisions.
    file_path = os.path.join("uploads", unique_filename) #Copies the uploaded image into the uploads folder.

    # Save image to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Save record in database
    new_image = UploadedImage(
    filename=image.filename,
    filepath=file_path,
    user_id=current_user.id
)

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {
        "message": "Image uploaded successfully",
        "filename": new_image.filename,
        "filepath": new_image.filepath
    }

@app.get("/images")
def get_all_images(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    images = db.query(UploadedImage).filter(
        UploadedImage.user_id == current_user.id
    ).all()

    return [
        {
            "id": image.id,
            "filename": image.filename,
            "image_url": f"http://127.0.0.1:8000/{image.filepath.replace(os.sep,'/')}",
            "uploaded_at": image.uploaded_at,
            "user_id": image.user_id,
        }
        for image in images
    ]

print("Current working directory:", os.getcwd())
print("Uploads exists:", os.path.exists("uploads"))
print("Uploads folder:", os.path.abspath("uploads"))

