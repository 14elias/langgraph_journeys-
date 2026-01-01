from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from typing import Annotated, List, Sequence, TypedDict
from dotenv import load_dotenv
import os


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


@tool
def add(a: int, b:int):
    """This is an addition function that adds 2 numbers together"""

    return a + b 

@tool
def subtract(a: int, b: int):
    """Subtraction function"""
    return a - b

@tool
def multiply(a: int, b: int):
    """Multiplication function"""
    return a * b

tools = [add, subtract, multiply]


model = init_chat_model(
    model="gpt-4o-mini"
).bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def process(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )

    response = model.invoke([system_prompt] + state['messages'])

    return {"messages": [response]}

def should_continue(state: AgentState):
    latest_message = state['messages'][-1]
    if latest_message.tool_calls:
        return 'continue'
    else:
        return 'end'
    

builder = StateGraph(AgentState)
builder.add_node('process', process)
builder.add_node('tools', ToolNode(tools=tools))

builder.add_edge(START, 'process')
builder.add_conditional_edges(
    'process',
    should_continue,
    {
        'continue':'tools',
        'end':END
    }
)

builder.add_edge('tools', 'process')

graph = builder.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
if __name__ == '__main__':
    inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
    # result = graph.invoke({
    #     "messages": [HumanMessage(content=input("enter your question: "))]
    # })
    print_stream(graph.stream(inputs, stream_mode="values"))