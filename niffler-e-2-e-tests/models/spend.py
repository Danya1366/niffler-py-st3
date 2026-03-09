from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from models.category import CategoryAdd


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    currency: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: dict
    spendDate: str
    currency: str
