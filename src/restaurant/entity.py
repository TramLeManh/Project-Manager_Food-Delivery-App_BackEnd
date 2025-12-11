import uuid
from datetime import time, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DistrictEntity(BaseModel):
	id: str = Field()
	name: str


class RestaurantEntity(BaseModel):
	restaurant_id: str = Field(alias="restaurant_id", default_factory=lambda: str(uuid.uuid4()))
	owner_id: str = Field(alias="ownerId", default_factory=lambda: str(uuid.uuid4()))

	address: str
	district: int
	categories: List[int]

	name: str
	image: str = Field(alias="image_url")
	rating: Optional[float] = Field(alias="rating")
	openTime: str
	closeTime: str
	created_at: datetime

	class Config:
		populate_by_name = True
		json_encoders = {
			time: lambda t: t.strftime("%H:%M")
		}
