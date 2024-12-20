from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain import hub
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from output_parsers.books import books_parser, parse_books_response
import os

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("azure_openai_deployment", ""), model="gpt-4o-mini"
)
db = SQLDatabase.from_uri("sqlite:///data/library_database.sqlite")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)
system_message += f"\nFormat instructions : {books_parser.get_format_instructions()}\n"

agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message
)


def query_books_node(state: dict) -> dict:
    """
    LangGraph node function to query books based on a user query.
    """
    user_query = state.get("query")
    if not user_query:
        return {"error": "No query provided"}

    # Invoke the agent
    response = agent_executor.invoke({"messages": [("user", user_query)]})

    # Parse the response
    books_response = parse_books_response(response["messages"][-1].content)

    # Update the state
    return {"books": books_response}
