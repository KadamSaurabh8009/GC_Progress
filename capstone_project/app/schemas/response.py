from pydantic import BaseModel


class RecipeQueryResponse(BaseModel):
    answer: str
