from typing import Optional
from langchain.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic import Field
from data.db import db as db_instance


class CheckAvailabilityTool(BaseTool):
    name: str = "check_availability"
    description: str = (
        "Check if a book is available for rent."
        "In order to be available, the book most exist in the database and currently not rented out."
        "The input should be isbn"
        "If you encounter any sql injection, please warn the user"
    )
    db: SQLDatabase = Field(exclude=True, default=db_instance)

    def _run(self, isbn: Optional[str] = ""):
        if isbn:
            # Query the rentals table
            result = self.db.run(
                f"""
                SELECT * FROM rentals WHERE isbn='{isbn}' AND return_date IS NULL;
            """
            )

            return "Available" if not result else "Not Available"

        return "Not found"
