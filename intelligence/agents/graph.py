from langgraph.graph import StateGraph, START, END

from intelligence.agents.state import QuantMindState
from intelligence.agents.nodes.approval import approval_node
from intelligence.agents.nodes.safe_nodes import (
    safe_market_analyst,
    safe_risk_analyst,
    safe_news_analyst,
    safe_quantitative_analyst,
)

from intelligence.agents.nodes.analysis_gate import (
    analysis_gate,
    route_after_analysis,
    analysis_error,
)

from intelligence.agents.nodes.decision_analyst import decision_analyst
from intelligence.agents.nodes.portfolio_manager import portfolio_manager


def build_graph(checkpointer=None):
    graph = StateGraph(QuantMindState)

    # Register nodes
    graph.add_node("market_analyst", safe_market_analyst)
    graph.add_node("risk_analyst", safe_risk_analyst)
    graph.add_node("news_analyst", safe_news_analyst)
    graph.add_node("quantitative_analyst", safe_quantitative_analyst)

    graph.add_node("analysis_gate", analysis_gate)
    graph.add_node("analysis_error", analysis_error)

    graph.add_node("decision_analyst", decision_analyst)
    graph.add_node("portfolio_manager", portfolio_manager)
    graph.add_node("approval", approval_node)

    # Parallel analysis
    graph.add_edge(START, "market_analyst")
    graph.add_edge(START, "risk_analyst")
    graph.add_edge(START, "news_analyst")
    graph.add_edge(START, "quantitative_analyst")

    # Wait for all four analysts before checking their results.
    graph.add_edge(
        [
            "market_analyst",
            "risk_analyst",
            "news_analyst",
            "quantitative_analyst",
        ],
        "analysis_gate",
    )

    # Conditional routing
    graph.add_conditional_edges(
        "analysis_gate",
        route_after_analysis,
        {
            "continue": "decision_analyst",
            "failed": "analysis_error",
        },
    )

    graph.add_edge("analysis_error", END)
    graph.add_edge("decision_analyst", "portfolio_manager")
    graph.add_edge("portfolio_manager", "approval")
    graph.add_edge("approval", END)

    return graph.compile(checkpointer=checkpointer)
