from pydantic import BaseModel
import os

class Currency(BaseModel):
    """Currency Schema (in reference to USD)"""
    name: str
    symbol: str
    code: str
    exchange_rate: float # Against USD

    def to_usd(self, amount: float):
        return amount * self.exchange_rate



default_currency = Currency(
    name="Indian Rupees",
    symbol="₹",
    code="INR",
    exchange_rate=float(os.getenv('DEF_CUR_EX_RATE', 0.012))
)

