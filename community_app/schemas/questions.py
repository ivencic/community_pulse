from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=15)
    category: CategoryBase


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: CategoryBase

    class Config:
        from_attributes = True

