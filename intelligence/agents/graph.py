from langgraph.graph import StateGraph, START, END
from intelligence.agents.state import QuantMindState
from intelligence.agents.nodes.market_analyst import market_analyst
from intelligence.agents.nodes.risk_analyst import risk_analyst
from intelligence.agents.nodes.news_analyst import news_analyst
from intelligence.agents.nodes.decision_analyst import decision_analyst
from intelligence.agents.nodes.approval import approval_node
from intelligence.agents.routing import route_after_approval

def build_graph(checkpointer=None):
    graph = StateGraph(QuantMindState)

    # Register nodes
    graph.add_node("market_analyst", market_analyst)
    graph.add_node("risk_analyst", risk_analyst)
    graph.add_node("news_analyst", news_analyst)
    graph.add_node("decision_analyst", decision_analyst)
    graph.add_node("approval", approval_node)
    # Parallel fan-out
    graph.add_edge(START, "market_analyst")
    graph.add_edge(START, "risk_analyst")
    graph.add_edge(START, "news_analyst")

    # Fan-in: wait for all three analysts
    graph.add_edge("market_analyst", "decision_analyst")
    graph.add_edge("risk_analyst", "decision_analyst")
    graph.add_edge("news_analyst", "decision_analyst")

    graph.add_edge("decision_analyst", "approval")
    graph.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "approved": END,
            "rejected": END,
        },
    )

    return graph.compile(checkpointer=checkpointer)

