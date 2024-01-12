from models import Product
from pydantic import BaseModel


class ComparedResult(BaseModel):
    product: Product
    current_price: float
    result: bool
    increase_percentage: float
