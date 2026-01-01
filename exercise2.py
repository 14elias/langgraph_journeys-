from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    number1: int
    operation1: str
    number2: int
    number3: int
    operation2: str
    number4: int
    final_number1: int
    final_number2: int

def add_node(state: AgentState) -> AgentState:
    '''adding number1 and number2 in the given state'''
    state['final_number1'] = state['number1'] + state['number2']

    return state

def subtract_node(state: AgentState) -> AgentState:
    """subtract number2 from number1 in the given state"""
    state['final_number1'] = state['number1'] - state['number2']

    return state

def router(state:AgentState):
    """deciding which node to be executed next"""

    if state['operation1'] == '+':
        return 'add_operation'
    elif state['operation1'] == '-':
        return 'subtract_operation'
    

def add_node2(state: AgentState) -> AgentState:
    '''adding number1 and number2 in the given state'''
    state['final_number2'] = state['number3'] + state['number4']

    return state

def subtract_node2(state: AgentState) -> AgentState:
    """subtract number2 from number1 in the given state"""
    state['final_number2'] = state['number3'] - state['number4']

    return state

def router2(state:AgentState):
    """deciding which node to be executed next"""

    if state['operation2'] == '+':
        return 'add_operation2'
    elif state['operation2'] == '-':
        return 'subtract_operation2'
    

graph = StateGraph(AgentState)
graph.add_node('add', add_node)
graph.add_node('subtract', subtract_node)
graph.add_node('router', lambda state:state)
graph.add_node('add2', add_node2)
graph.add_node('subtract2', subtract_node2)
graph.add_node('router2', lambda state:state)

graph.add_edge(START, 'router')
graph.add_conditional_edges(
    'router',
    router,
    {
        'add_operation': 'add',
        'subtract_operation':'subtract'
    }
)
graph.add_edge('add', 'router2')
graph.add_edge('subtract', 'router2')
graph.add_conditional_edges(
    'router2',
    router2,
    {
        'add_operation2': 'add2',
        'subtract_operation2': 'subtract2'
    }
)

graph.add_edge('add2', END)
graph.add_edge('subtract2', END)

compiled = graph.compile()
data = {
    'number1':10,
    'operation1':'-',
    'number2':5,
    'number3':7,
    'number4':2,
    'operation2':'+',
    'final_number1':0,
    "final_number2":0

}
# result = compiled.invoke(data)
# print(result)

if __name__ == '__main__':
    from IPython.display import Image, display
    display(Image(compiled.get_graph().draw_mermaid_png()))