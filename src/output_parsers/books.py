from typing import Dict, Any
import json
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Book(BaseModel):
    isbn: str = Field(description="ISBN of the book")
    title: str = Field(description="title of the book")
    category: str = Field(description="category of the book")
    author: str = Field(description="author of the book")
    publisher: str = Field(description="publisher of the book")
    price: float = Field(description="rental price of the book")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "isbn": self.isbn,
            "title": self.title,
            "category": self.category,
            "author": self.author,
            "publisher": self.publisher,
            "price": self.price,
        }


class BooksResponse(BaseModel):
    books: list[Book] = Field(description="A list of books that match the query")


books_parser = PydanticOutputParser(pydantic_object=BooksResponse)


def parse_books_response(response: str) -> BooksResponse:
    js = json.loads(response)
    books = [Book(**book) for book in js["books"]]

    return BooksResponse(books=books)
