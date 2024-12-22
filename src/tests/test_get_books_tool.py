from tools.get_books_tool import GetBooksTool
from unittest.mock import MagicMock
import pytest
import json


def test_get_books_tool():
    # Mock the database instance
    db_mock = MagicMock()

    # Mock the database run method to return sample data
    db_mock.run.return_value = str(
        [
            (
                "Harry Potter",
                "Fantasy",
                "J.K. Rowling",
                "Bloomsbury",
                10,
            ),
        ]
    )

    # Create an instance of GetBooksTool and inject the mock database
    tool = GetBooksTool()
    tool.db = db_mock

    # Test case 1: Search with specific filters
    json_input = json.dumps(
        {
            "book_title": "Harry",
            "category": "Fantasy",
            "author": "J.K.",
            "publisher": "Bloomsbury",
            "min_price": 5,
            "max_price": 15,
        }
    )
    result = tool._run(json_input)

    # Verify that the query was executed correctly
    db_mock.run.assert_called_once_with(
        """SELECT * FROM books WHERE lower(book_title) LIKE '%harry%' 
            AND category LIKE '%fantasy%' 
            AND lower(author) LIKE '%j.k.%' 
            AND lower(publisher) LIKE '%bloomsbury%' 
            AND rental_price BETWEEN 5 AND 15
            """
    )

    # Verify the result is as expected
    assert "Harry" in result


def test_get_books_tool_edge_cases():
    # Mock the database instance
    db_mock = MagicMock()

    # Mock the database run method to return no data
    db_mock.run.return_value = ""

    # Create an instance of GetBooksTool and inject the mock database
    tool = GetBooksTool()
    tool.db = db_mock

    # Test case: No books match the query
    json_input = json.dumps(
        {
            "book_title": "Nonexistent Book",
            "category": "Nonexistent Category",
        }
    )
    result = tool._run(json_input)

    # Verify that the query was executed correctly
    db_mock.run.assert_called_once_with(
        """SELECT * FROM books WHERE lower(book_title) LIKE '%nonexistent book%' 
            AND category LIKE '%nonexistent category%' 
            AND lower(author) LIKE '%%' 
            AND lower(publisher) LIKE '%%' 
            AND rental_price BETWEEN 0 AND 1000
            """
    )

    # Verify the result is an empty list
    assert result == ""
