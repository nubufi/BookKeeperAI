from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain import hub
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from output_parsers import books_parser
import os

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI model
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("azure_openai_deployment", ""), model="gpt-4o-mini"
)

# Connect to SQLite database
db = SQLDatabase.from_uri("sqlite:///data/library_database.sqlite")

# Create the SQL database toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Pull LangChain system prompt for SQL interaction
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)

# Define a function to format and parse the output using books_parser
def format_books_output(output: str) -> dict:
    """
    Format the raw output using the books_parser.
    """
    parsed_output = books_parser.parse(output)  # Ensure books_parser has a parse method
    return parsed_output

# Create the agent
agent_executor = create_react_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    system_message=system_message
)

# Example query function
def query_books_table(user_query: str):
    """
    Query the books table based on the user query and return structured output.
    """
    try:
        # Invoke the agent with the query
        response = agent_executor.invoke({"input": user_query})
        
        # Extract and format the agent's output
        formatted_output = format_books_output(response['output'])
        return formatted_output
    
    except Exception as e:
        return {"error": str(e)}

# Example Usage
if __name__ == "__main__":
    # Example user query
    user_query = "Show me all books in the science fiction category with rental prices below $15."

    # Get the structured response
    result = query_books_table(user_query)
    print("Formatted Output:")
    print(result)
