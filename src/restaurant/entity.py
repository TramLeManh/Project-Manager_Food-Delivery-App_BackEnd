import uuid
from datetime import time, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CategoryEntity(BaseModel):
	id: str = Field(default_factory=lambda: str(uuid.uuid4()))
	name: str


class DistrictEntity(BaseModel):
	id: str = Field()
	name: str



class RestaurantEntity(BaseModel):
	id: str = Field(alias="_id", default_factory=lambda: str(uuid.uuid4()))
	owner_id: str = Field(alias="ownerId", default_factory=lambda: str(uuid.uuid4()))

	address: str
	district: DistrictEntity
	categories: List[CategoryEntity]

	name: str
	image: str = Field(alias="image_url")
	rating: Optional[float] = Field(alias="rating")
	openTime: time
	closeTime: time
	created_at: datetime

	class Config:
		populate_by_name = True
		json_encoders = {
			time: lambda t: t.strftime("%H:%M")
		}
