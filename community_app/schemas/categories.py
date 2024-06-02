from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    text: str = Field(..., min_length=15)


class CategoryResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True
