from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the state
class State(TypedDict):
    message: str


# 2. Define a node
def greeting(state: State):
    return {
        "message": state["message"] + " Welcome to LangGraph!"
    }


# 3. Build the graph
builder = StateGraph(State)

builder.add_node("greeting", greeting)

builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)


# 4. Compile
graph = builder.compile()


# 5. Execute
result = graph.invoke({
    "message": "Hello"
})

print(result)