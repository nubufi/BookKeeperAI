from langchain_community.utilities.sql_database import SQLDatabase
import os

file_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(file_path, "library_database.sqlite")

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
