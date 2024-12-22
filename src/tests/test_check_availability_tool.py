from tools.check_availability_tool import CheckAvailabilityTool
from unittest.mock import MagicMock
import pytest


def test_check_availability_tool():
    # Mock database connection
    db_mock = MagicMock()

    # Mock query results for different scenarios
    db_mock.run.return_value = []  # Empty result implies "Available"
    tool = CheckAvailabilityTool()
    tool.db = db_mock

    # Test when book is available
    result = tool._run(isbn="9781234567890")
    assert result == "Available"

    # Test when book is not available
    db_mock.run.return_value = [{"isbn": "9781234567890", "return_date": None}]
    result = tool._run(isbn="9781234567890")
    assert result == "Not Available"

    # Test when ISBN is not provided
    result = tool._run(isbn="")

    assert result == "Not found"
