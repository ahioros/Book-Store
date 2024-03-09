import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(debug=True)


class BookCreate(BaseModel):
    title: str
    author: str
    topic: str


class Book(BookCreate):
    id: int


class CreateTable(BaseModel):
    create: bool


def create_connection():
    connection = sqlite3.connect("bookstore.db")
    return connection


def fill_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, topic TEXT)"
    )
    connection.commit()
    connection.close()


def creation_book(book: BookCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, topic) VALUES (?,?,?)",
        (book.title, book.author, book.topic),
    )
    connection.commit()
    connection.close()


def read_book():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    Books = cursor.fetchall()
    connection.close()

    booklist = [
        Book(id=book[0], title=book[1], author=book[2], topic=book[3]) for book in Books
    ]

    return booklist


@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API example!"}


@app.post("/book/")
def create_book_endpoint(book: BookCreate):
    book_id = creation_book(book)
    return {"id": book_id, **book.dict()}


@app.post("/table/")
def create_table(create: CreateTable):
    if create:
        fill_table()
    return {"message": "Table created"}


@app.get("/books/")
def get_books():
    return read_book()
