from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import User
from .schemas import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def home():
    return {
        "message": "DevTrack API is running"
    }


@app.get("/test-db")
def test_database():
    return {
        "message": "Database connected successfully"
    }

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
    name=user.name,
    email=user.email,
    password=user.password,
    role=user.role
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }
