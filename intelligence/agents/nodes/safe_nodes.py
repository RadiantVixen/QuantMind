
from intelligence.agents.nodes.market_analyst import market_analyst
from intelligence.agents.nodes.risk_analyst import risk_analyst
from intelligence.agents.nodes.news_analyst import news_analyst
from intelligence.agents.nodes.quantitative_analyst import quantitative_analyst


def safe_market_analyst(state):
    try:
        return market_analyst(state)
    except Exception as e:
        return {"market_error": str(e)}


def safe_risk_analyst(state):
    try:
        return risk_analyst(state)
    except Exception as e:
        return {"risk_error": str(e)}


def safe_news_analyst(state):
    try:
        return news_analyst(state)
    except Exception as e:
        return {"news_error": str(e)}


def safe_quantitative_analyst(state):
    try:
        return quantitative_analyst(state)
    except Exception as e:
        return {"quant_error": str(e)}
