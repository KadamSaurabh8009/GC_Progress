from pydantic import BaseModel
from typing import Optional


class RecipeQueryRequest(BaseModel):
    query: str
    cuisine: Optional[str] = "Any"
    max_time: Optional[int] = None
    veg_only: Optional[bool] = False
