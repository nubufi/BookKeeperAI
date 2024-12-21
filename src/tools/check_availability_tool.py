from typing import Optional
from langchain.tools import BaseTool
from data.db import db


class CheckAvailabilityTool(BaseTool):
    name: str = "check_availability"
    description: str = (
        "Check if a book is available for rent."
        "In order to be available, the book most exist in the database and currently not rented out."
        "The input should be isbn"
    )

    def _run(self, isbn: Optional[str] = ""):
        if isbn:
            # Query the rentals table
            result = db.run(
                f"""
                SELECT * FROM rentals WHERE isbn='{isbn}' AND return_date IS NULL;
            """
            )

            return "Available" if not result else "Not Available"

        return "Not found"
