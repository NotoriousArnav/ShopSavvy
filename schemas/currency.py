from pydantic import BaseModel

class Currency(BaseModel):
    """Currency Schema (in reference to USD)"""
    name: str
    symbol: str
    code: str
    exchange_rate: float

    def to_usd(self, amount: float):
        return amount * self.exchange_rate



default_currency = Currency(
    name="Indian Rupees",
    symbol="₹",
    code="INR",
    exchange_rate=0.012
)

