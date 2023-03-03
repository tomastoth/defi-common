from beanie import Document
from pydantic import BaseModel


class Trade(BaseModel):
    timestamp: str
    coin_symbol: str
    is_buy: bool
    size_eth: float
    price: float
    profit: float | None


class TraderUpdate(Document):
    number_of_trades: int
    traded_eth: float
    average_trade_size: float
    trades: list[Trade]
    trader_address: str
    sum_profit: float
