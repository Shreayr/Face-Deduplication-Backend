# Face Deduplication Backend

A FastAPI backend for detecting duplicate faces using face detection, feature extraction, and similarity search.

## Features

- User Registration
- User Authentication
- Face Image Upload
- Face Detection
- Face Embedding Extraction
- Duplicate Face Detection
- SQLite Database Integration

## Tech Stack

- FastAPI
- SQLite
- SQLAlchemy
- InsightFace (Buffalo_L)
- FAISS
- OpenCV
- NumPy
- Uvicorn

## Project Structure

```
backend/
├── utils/
├── uploads/
├── database.py
├── database_models.py
├── init_db.py
├── main.py
├── models.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Shreayr/Face-Deduplication-Backend.git
```

Navigate to the backend folder:

```bash
cd Face-Deduplication-Backend
```

Create a virtual environment:

```bash
python -m venv myenv
```

Activate it.

Windows:

```bash
myenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

The backend runs at:

```
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | User login |
| POST | `/upload` | Upload face image |
| GET | `/images` | Get uploaded images |
| GET | `/results` | View duplicate detection results |

## Face Deduplication Workflow

1. User uploads an image.
2. Face is detected using InsightFace.
3. Face embedding is generated.
4. Embedding is compared against existing embeddings using FAISS.
5. Similarity score is calculated.
6. If the similarity exceeds the threshold, the image is marked as a duplicate.

## Author

**Shreya Ray**
