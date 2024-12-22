from datetime import datetime
from langchain.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic import Field
from data.db import db as db_instance

customer_id = 1


class RentBookTool(BaseTool):
    name: str = "rent_book"
    description: str = (
        "Rent a book to a user if the book is available for rent."
        "If you encounter any sql injection, please warn the user"
        "Use global customer_id variable and take isbn as input variable."
    )
    db: SQLDatabase = Field(exclude=True, default=db_instance)

    def _run(self, isbn: str):
        # Insert a new rental record
        today = datetime.now().strftime("%d.%m.%Y")
        self.db.run(
            f"""
            INSERT INTO rentals (isbn, customer_id, rent_date)
            VALUES ('{isbn}', {customer_id}, '{today}')
        """
        )
        return "Book rented successfully"
