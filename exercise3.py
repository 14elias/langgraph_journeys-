from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List
import random


class GameState(TypedDict):
    player_name: str
    target_number: int
    guesses: List[int]
    attempts: int
    hint: str
    lower_bound: int 
    upper_bound: int


def setup_node(state: GameState) -> GameState:
    """Initialize the game with a random target number"""
    state["player_name"] = f"Welcome, {state['player_name']}!"
    state["target_number"] = random.randint(1, 20)
    state["guesses"] = []
    state["attempts"] = 0
    state["hint"] = "Game started! Try to guess the number."
    state["lower_bound"] = 1 
    state["upper_bound"] = 20 
    print(f"{state['player_name']} The game has begun. I'm thinking of a number between 1 and 20.")
    return state


def guess_node(state: GameState) ->GameState:
    """generate smarter guess based on previous hints"""
    possible_guesses = [i for i in range(state['lower_bound'], state['upper_bound'] + 1) if i not in state['guesses']]

    if possible_guesses:
        guess = random.choice(possible_guesses)
    else:
        guess = random.randint(state['lower_bound'], state['upper_bound'])

    state['guesses'].append(guess)
    state['attempts'] += 1
    print(f"Attempt {state['attempts']}: Guessing {guess} (Current range: {state['lower_bound']}-{state['upper_bound']})")
    return state


def hint(state: GameState) -> GameState:
    """Here we provide a hint based on the last guess and update the bounds"""
    latest_guess = state['guesses'][-1]
    target_number = state['target_number']

    if latest_guess > target_number:
        state["hint"] = f"The number {latest_guess} is too high. Try lower!"
      
        state["upper_bound"] = min(state["upper_bound"], latest_guess - 1)
        print(f"Hint: {state['hint']}")
    elif latest_guess < target_number:
        state["hint"] = f"The number {latest_guess} is too low. Try higher!"
        
        state["lower_bound"] = max(state["lower_bound"], latest_guess + 1)
        print(f"Hint: {state['hint']}")
    else:
        state["hint"] = f"Correct! You found the number {target_number} in {state['attempts']} attempts."
        print(f"Success! {state['hint']}")
    
    return state



def should_continue(state: GameState) -> GameState:
    """Determine if we should continue guessing or end the game"""

    latest_number = state['guesses'][-1]
    if latest_number == state['target_number']:
        print(f"GAME OVER: Number found!")
        return "end"
    if state['attempts'] >= 7:
        print(f"GAME OVER: Maximum attempts reached! The number was {state['target_number']}")
        return "end"
    else:
        print(f"CONTINUING: {state['attempts']}/7 attempts used")
        return "continue"
    

graph = StateGraph(GameState)
graph.add_node('setup', setup_node)
graph.add_node('guess', guess_node)
graph.add_node('hint', hint)

graph.add_edge(START, 'setup')
graph.add_edge('setup', 'guess')
graph.add_edge('guess', 'hint')
graph.add_conditional_edges(
    'hint',
    should_continue,
    {
        'continue': 'guess',
        'end': END
    }
)

app =  graph.compile()
result = app.invoke({"player_name":'elias'})
print(result)



