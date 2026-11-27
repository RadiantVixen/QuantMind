
from dataclasses import dataclass


@dataclass
class MarketDataConfig:
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    limit: int = 500


@dataclass
class MarketDataSchema:
    timestamp: str = "timestamp"
    open: str = "open"
    high: str = "high"
    low: str = "low"
    close: str = "close"
    volume: str = "volume"

    @property
    def columns(self) -> list[str]:
        return [
            self.timestamp,
            self.open,
            self.high,
            self.low,
            self.close,
            self.volume,
        ]
