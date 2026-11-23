from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class AssistantState(TypedDict):
    request: str
    task_type: str
    result: str
    response: str


# NODE 1
def classify_request(state: AssistantState):
    request = state["request"].lower()

    if "calculate" in request or "average" in request:
        task_type = "calculation"
    elif "what" in request or "why" in request:
        task_type = "question"
    elif "search" in request or "find" in request or "look up" in request:
        task_type = "search"
    else:
        task_type = "other"

    return {"task_type": task_type}


def calculation(state: AssistantState):

    return {"result": "Performed calculation based on request."}

def question(state: AssistantState):
    return {"result": "Answered the question based on request."}

def search(state: AssistantState):
    return {"result": "Performed search based on request."}

def other(state: AssistantState):
    return {"result": "Handled other types of requests."}

# NODE 2
def process_request(state: AssistantState):
    task_type = state["task_type"]

    if task_type == "calculation":
        result = "Calculation processed"

    elif task_type == "question":
        result = "Question processed"

    elif task_type == "search":
        result = "Search processed"

    else:
        result = "Unknown task"

    return {"result": result}


# NODE 3
def generate_response(state: AssistantState):
    return {
        "response": f"Your request was classified as "
                    f"{state['task_type']}. "
                    f"{state['result']}."
    }


# ROUTING FUNCTION
def route_request(state: AssistantState):
    return state["task_type"]

# CREATE GRAPH
builder = StateGraph(AssistantState)


# REGISTER NODES
builder.add_node("classify", classify_request)
builder.add_node("process", process_request)
builder.add_node("generate", generate_response)
builder.add_node("calculation", calculation)
builder.add_node("question", question)
builder.add_node("search", search)
builder.add_node("other", other)





# CONNECT NODES
builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_request,
    {
        "calculation": "calculation",
        "question": "question",
        "search": "search",
        "other": "other"
    }
)

builder.add_edge("calculation", "process")
builder.add_edge("question", "process")
builder.add_edge("search", "process")
builder.add_edge("other", "process")
builder.add_edge("process", "generate")
builder.add_edge("generate", END)


graph = builder.compile()

initial_state = {
    "request": "Calculate average of 10, 20, 30",
    "task_type": "",
    "result": "",
    "response": ""
}

output = graph.invoke(initial_state)

print(output)

