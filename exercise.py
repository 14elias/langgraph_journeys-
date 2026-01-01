from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    name: str
    age: int
    skills: list[str]
    result: str


def personalize_name(state: AgentState) -> AgentState:
    state['result'] = f'{state['name']} wellcome to the system! '

    return state

def describe_age(state: AgentState) -> AgentState:
    state['result'] += f'you are {state['age']}! '
    return state

def user_skill(state: AgentState) -> AgentState:
    skills = ','.join(state['skills'])
    state['result'] += f'you have skills  in: {skills}'

    return state

graph = StateGraph(AgentState)

graph.add_node('name', personalize_name)
graph.add_node('age', describe_age)
graph.add_node('skill', user_skill)

graph.set_entry_point('name')
graph.add_edge('name','age')
graph.add_edge('age','skill')
graph.set_finish_point('skill')

compliled = graph.compile()
result = compliled.invoke({'name':'elias', 'age':'23', 'skills':['python', 'c++', 'DSA']})
print(result['result'])
