from datetime import datetime
from pydantic import BaseModel


class SaveToMenu(BaseModel):
    username: str
    filters: list | None = None
    recipes: list
    created_at: datetime = datetime.now()
