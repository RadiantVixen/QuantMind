
import pandas as pd


def backtest(
    df: pd.DataFrame,
    predictions,
    transaction_cost: float = 0.001,
) -> pd.DataFrame:
    """
    Long-only strategy:
    Buy when prediction is UP.
    Otherwise stay in cash.
    """

    results = df.copy()

    # Position decided at candle close t
    # Return realized over candle t+1
    results["position"] = predictions

    results["next_return"] = (
        results["close"].shift(-1) / results["close"] - 1
    )

    # Cost when entering or exiting a position
    results["trade"] = (
        results["position"].diff().abs()
    )
    results["trade"] = results["trade"].fillna(
        results["position"].abs()
    )

    results["strategy_return"] = (
        results["position"] * results["next_return"]
        - results["trade"] * transaction_cost
    )

    results["equity"] = (
        1 + results["strategy_return"].fillna(0)
    ).cumprod()

    return results



def calculate_performance(results: pd.DataFrame) -> dict:
    returns = results["strategy_return"].dropna()

    total_return = results["equity"].iloc[-1] - 1

    volatility = returns.std() * (24 * 365) ** 0.5

    sharpe = (
        (returns.mean() / returns.std()) * (24 * 365) ** 0.5
        if returns.std() != 0 else 0
    )

    drawdown = (
        results["equity"] / results["equity"].cummax() - 1
    )

    return {
        "total_return": total_return,
        "annualized_volatility": volatility,
        "sharpe_ratio": sharpe,
        "max_drawdown": drawdown.min(),
    }

