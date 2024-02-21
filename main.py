from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel


DATABASE_URL = "postgresql://postgres:ines@localhost:5432/fastapi_db"


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()


Base = declarative_base()

class Book(Base):
    __tablename__ = "book"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)


Base.metadata.create_all(bind=engine)


class BookCreate(BaseModel):
    title: str
    description: str

class BookUpdate(BaseModel):
    title: str
    description: str

class BookResponse(BaseModel):
    id: int
    title: str
    description: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.id == id).first()

def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

# Routes
@app.post("/books/", response_model=BookResponse)
def create_book_route(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(book, db)

@app.get("/books/", response_model=list[BookResponse])
def get_books_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(skip, limit, db)

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_route(book_id: int, db: Session = Depends(get_db)):
    return get_book(book_id, db)

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book_route(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    return update_book(book_id, book, db)

@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book_route(book_id: int, db: Session = Depends(get_db)):
    return delete_book(book_id, db)
