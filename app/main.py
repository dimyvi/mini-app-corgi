from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import OperationalError
import time, os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/corgi_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    description = Column(String, nullable=False)

def init_db():
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            photos_data = [
                {"filename": "corgi1.jpg", "description": "Валлийский пемброк"},
                {"filename": "corgi2.jpg", "description": "Валлийский кардиган"}
            ]
            for data in photos_data:
                photo = db.query(Photo).filter(Photo.filename == data["filename"]).first()
                if photo:
                    photo.description = data["description"]
                else:
                    db.add(Photo(**data))
            db.commit()
            db.close()
            break
        except OperationalError:
            time.sleep(2)

init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/info", response_class=HTMLResponse)
def info(request: Request, db: Session = Depends(get_db)):
    photos = db.query(Photo).all()
    return templates.TemplateResponse("info.html", {"request": request, "photos": photos})
