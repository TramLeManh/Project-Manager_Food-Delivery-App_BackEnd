# python
# src/articles/model.py
from datetime import time, date, datetime

from pydantic import BaseModel, Field, validator


class Article(BaseModel):
    article_id: str = Field(..., alias="id")
    title: str = Field(...)
    image: str = Field(...)
    content: str = Field(...)
    date: datetime = Field(..., alias="date")
    category: str = Field(...,alias="category")

    @validator("date", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d-%m-%Y")
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%d, %b, %Y")  # e.g. 24, Nov, 2025
        }
