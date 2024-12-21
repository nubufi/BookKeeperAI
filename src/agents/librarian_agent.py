from langchain_openai import AzureChatOpenAI
from tools.get_books_tool import GetBooksTool
from tools.check_availability_tool import CheckAvailabilityTool
from tools.rent_book_tool import RentBookTool
from langgraph.prebuilt import create_react_agent
import os

llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("azure_openai_deployment", ""), model="gpt-4o-mini"
)


tools = [GetBooksTool(), CheckAvailabilityTool(), RentBookTool()]
agent = create_react_agent(llm, tools)
