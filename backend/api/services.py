from intelligence.agents.graph import build_graph
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver
from intelligence.agents.graph import build_graph
import uuid
from langgraph.types import Command

ROOT_DIR = Path(__file__).resolve().parents[2]

connection = sqlite3.connect(
    ROOT_DIR / "quantmind_checkpoints.sqlite",
    check_same_thread=False,
)

checkpointer = SqliteSaver(connection)
checkpointer.setup()

quantmind_graph = build_graph(checkpointer=checkpointer)


def format_result(result):
    fields = [
        "symbol",
        "latest_price",
        "prediction",
        "probability_up",
        "probability_down",
        "risk_analysis",
        "news_analysis",
        "news_sentiment",
        "news_sentiment_score",
        "decision",
        "decision_score",
        "analyst_agreement",
        "explanation",
        "risk_budget",
        "recommended_position_value",
        "recommended_position_units",
        "estimated_max_loss",
        "portfolio_exposure_after_trade_pct",
        "quant_trend",
        "quant_rsi",
        "quant_momentum",
        "quant_volatility_regime",
        "quant_support",
        "quant_resistance",
        "quant_analysis",
        "status",
        "analyst_errors",
        "approval_status",
        "risk_level",
    ]

    return {
        key: result[key]
        for key in fields
        if key in result
    }



def run_analysis(initial_state):

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = quantmind_graph.invoke(initial_state, config=config)

    if result.get("analysis_status") == "FAILED":
        return {
            "status": "FAILED",
            "error": result.get("analysis_error"),
            "thread_id": thread_id,
        }

    interrupts = result.get("__interrupt__", [])

    approval_request = (
        interrupts[0].value
        if interrupts else None
    )

    return {
        **format_result(result),
        "thread_id": thread_id,
        "approval_required": bool(interrupts),
        "approval_request": approval_request,
    }


def resume_analysis(thread_id, approved):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = quantmind_graph.invoke(
        Command(resume={"approved": approved}),
        config=config,
    )

    return {
        **format_result(result),
        "thread_id": thread_id,
        "approval_required": False,
    }