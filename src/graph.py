import langchain
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import sqlite3
from langgraph.prebuilt import create_react_agent, ToolNode
from typing import TypedDict
from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from agents.librarian_agent import query_books_node
from langgraph.checkpoint.memory import MemorySaver
import os

load_dotenv()


@tool
def search_books(query: str) -> str:
    """Call this tool to search for books in the database or library"""
    print(f"Searching for {query} in the database")

    return "Harry Potter"


@tool
def get_book_info(book: str) -> str:
    """Call this tool to get the information of a book"""
    print(f"Getting information of {book}")

    return "Harry Potter is a fantasy novel written by British author J. K. Rowling."


@tool
def check_availability(book: str) -> str:
    """Call this tool to check the availability of a book"""
    print(f"Checking availability of {book}")

    return "The book is available"


@tool
def rent_book(book: str) -> str:
    """Call this tool to rent a book"""
    print(f"Renting {book}")

    return "You have successfully rented the book"


def sql_query_generator(query: str):
    """Generate a SQL query based on the user query"""
    return {
        "messages": [AIMessage(f"SELECT * FROM books WHERE title LIKE '%{query}%'")]
    }


def should_continue(state: MessagesState):
    """Return the next node to execute."""
    last_message = state["messages"][-1]
    # If there is no function call, then we finish
    print(last_message.tool_calls, "***")
    if not last_message.tool_calls:
        return END
    # Otherwise if there is, we continue
    return "sql"


tools = [search_books, get_book_info, check_availability, rent_book]
tool_node = ToolNode(tools)
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("azure_openai_deployment", ""), model="gpt-4o-mini"
)
model = llm.bind_tools(tools)
memory = MemorySaver()


# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}


# --- Workflow Definition ---
workflow = StateGraph(MessagesState)

# Add Nodes
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)
workflow.add_node("sql", sql_query_generator)

# Define Edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["sql", END])
workflow.add_edge("sql", "action")

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile(checkpointer=memory)
# Compile the workflow
graph = workflow.compile()


def run_query(query: str):
    config = {"configurable": {"thread_id": "2"}}
    input_message = HumanMessage(content=query)
    for event in app.stream(
        {"messages": [input_message]}, config, stream_mode="values"
    ):
        event["messages"][-1].pretty_print()


# --- Run LangGraph ---
def run_langgraph():
    while True:
        query = input("Enter your query: ")
        run_query(query)


# Run the workflow
if __name__ == "__main__":
    run_langgraph()
