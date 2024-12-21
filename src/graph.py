from agents.librarian_agent import agent
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


memory = MemorySaver()


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    output = agent.invoke(state)

    return {"messages": output["messages"]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "5"}}


def stream_event(user_query):
    # The config is the **second positional argument** to stream() or invoke()!
    events = graph.stream(
        {"messages": [("user", user_query)]}, config, stream_mode="values"
    )
    events_list = list(events)
    last_event = events_list[-1]

    return last_event["messages"][-1].content
