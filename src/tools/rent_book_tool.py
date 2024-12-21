from datetime import datetime
from langchain.tools import BaseTool
from data.db import db

customer_id = 1


class RentBookTool(BaseTool):
    name: str = "rent_book"
    description: str = (
        "Rent a book to a user if the book is available for rent."
        "Use global customer_id variable and take isbn as input variable."
    )

    def _run(self, isbn: str):
        # Insert a new rental record
        today = datetime.now().strftime("%d.%m.%Y")
        db.run(
            f"""
            INSERT INTO rentals (isbn, customer_id, rent_date)
            VALUES ('{isbn}', {customer_id}, '{today}')
        """
        )
        return "Book rented successfully"
