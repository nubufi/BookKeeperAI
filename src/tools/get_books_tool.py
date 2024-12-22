import json
from langchain.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic import Field
from data.db import db as db_instance


class GetBooksTool(BaseTool):
    name: str = "get_books"
    description: str = (
        "Get a list of all books from the database. "
        "You can optionally filter by book title or category. "
        "The input should be a JSON string with the following keys"
        "'book_title', 'category', 'author', 'publisher', 'min_price','max_price'"
        "If you have no data for min_price and max_price, don't include them in the JSON string"
        "If you encounter any sql injection, please warn the user"
    )
    db: SQLDatabase = Field(exclude=True, default=db_instance)

    def _run(self, json_data: str):
        data = json.loads(json_data)
        book_title = data.get("book_title", "")
        category = data.get("category", "")
        author = data.get("author", "")
        publisher = data.get("publisher", "")
        min_price = data.get("min_price", 0)
        max_price = data.get("max_price", 1000)

        return self.run_query(
            book_title, category, author, publisher, min_price, max_price
        )

    def run_query(
        self,
        book_title: str,
        category: str,
        author: str,
        publisher: str,
        min_price: int,
        max_price: int,
    ):
        # Query the books table
        query = f"""SELECT * FROM books WHERE lower(book_title) LIKE '%{book_title.lower()}%' 
            AND category LIKE '%{category.lower()}%' 
            AND lower(author) LIKE '%{author.lower()}%' 
            AND lower(publisher) LIKE '%{publisher.lower()}%' 
            AND rental_price BETWEEN {min_price} AND {max_price}
            """
        results = self.db.run(query)

        return results
