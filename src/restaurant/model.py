import uuid
from datetime import time
from typing import Optional, List

from anthropic import BaseModel
from pydantic import Field


class Category(BaseModel):
	id: str = Field(default_factory=lambda: str(uuid.uuid4()))
	name: str


class District(BaseModel):
	id: Optional[str]
	name: str


class RestaurantModel(BaseModel):
	restaurant_id: str = Field(..., alias="restaurantId")
	name: str
	address: Optional[str] = None
	district: Optional[District] = None
	picture: Optional[str] = None
	rating: float = 0.0
	openTime: Optional[str] = Field(None, alias="openTime")
	closeTime: Optional[str] = Field(None, alias="closeTime")
	categories: List[Category]

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class RestaurantFilter(BaseModel):
	category: Optional[str]
	district: Optional[str]


class RestaurantCreate(BaseModel):
	name: str
	address: Optional[str] = None
	description: Optional[str] = None
	district: Optional[District] = None
	image: Optional[str] = Field(None, alias="image_url")
	rating: float = 0.0
	open_time: time = Field(None, alias="openTime")
	close_time: time = Field(None, alias="closeTime")
	categories: list[Category]
