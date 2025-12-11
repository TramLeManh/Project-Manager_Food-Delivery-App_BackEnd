import uuid
from typing import Optional, List

from anthropic import BaseModel
from pydantic import Field


class Category(BaseModel):
	id: str = Field(default_factory=lambda: str(uuid.uuid4()))
	name: str


class District(BaseModel):
	id: Optional[str]
	name: str


class BaseRestaurantModel(BaseModel):
	restaurant_id: str = Field(..., alias="restaurantId")
	name: str


class RestaurantModel(BaseRestaurantModel):
	address: Optional[str] = None
	district: Optional[str] = None
	picture: Optional[str] = None
	rating: float = 0.0
	openTime: Optional[str] = Field(None, alias="openTime")
	closeTime: Optional[str] = Field(None, alias="closeTime")
	categories: List[str]

	model_config = {"json_schema_extra": {
		"examples": [
			{
				"restaurant_id": "c32b9038-24f4-4d2d-8e9b-8c1b67531c95",
				"name": "Phở Anh Hai",
				"address": "10 Đan Trường,  Quận 4, Thành phố Hồ Chí Minh",
				"district": "District 1",
				"picture": "https://cdn-media.sforum.vn/storage/app/media/Bookgrinder2/quan-pho-cua-anh-hai-1.jpg",
				"rating": 5.0,
				"openTime": "07:00",
				"closeTime": "22:00",
				"categories": [
					"Activity",
					"Bar"
				]
			},
		]
	},
		"allow_population_by_field_name": True,
		"orm_mode": True

	}


class RestaurantFilter(BaseModel):
	category: Optional[int]
	district: Optional[int]


class RestaurantCreate(BaseModel):
	name: str
	address: Optional[str] = None
	description: Optional[str] = None
	district_id: Optional[int] = None
	image: Optional[str] = Field(None, alias="image_url")
	rating: Optional[float] = 0.0
	open_time: Optional[str] = Field(None, alias="openTime")
	close_time: Optional[str] = Field(None, alias="closeTime")
	categories: List[int]

	class Config:
		allow_population_by_field_name = True
		json_schema_extra = {
			"examples": [
				{
					"name": "Example Restaurant",
					"address": "123 Example St",
					"description": "A cozy spot",
					"district_id": 1,
					"image_url": "https://example.com/image.jpg",
					"rating": 4.5,
					"openTime": "2025-12-02T01:00:00+00:00",
					"closeTime": "2025-12-02T15:00:00+00:00",
					"categories": [1, 2]
				}
			]
		}
