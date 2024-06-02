from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description="You need to provide question ID")
    is_agree: bool = Field(..., description="If False - disagree. If True - agree")


class StatisticResponse(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int
