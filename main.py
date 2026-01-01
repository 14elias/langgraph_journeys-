import langchain 
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    message: str 


def greeting_node(state: AgentState)->AgentState:
    """simple node that adds a greeting message to the node"""

    state['message'] = 'hey' + state['message'] + 'how is your day going'

    return state

graph = StateGraph(AgentState)
graph.add_node('greeter', greeting_node)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')

app = graph.compile()

print(app.invoke({"message":'bro'}))
def main():
    print(langchain.__version__)

from langchain.agents import create_agent
if __name__ == "__main__":
    main()
