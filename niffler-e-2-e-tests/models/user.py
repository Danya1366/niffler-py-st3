from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserName(BaseModel):
    username: str

class UserSql(SQLModel, table=True):
    __tablename__ = "user"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str

