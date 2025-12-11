from src.restaurant.entity import RestaurantEntity
from src.restaurant.model import RestaurantModel

categories: dict[int, str] = {
	1: "Activity",
	2: "Bar",
	3: "Bistro",
	4: "Brunch",
	5: "Cafe",
	6: "Club",
	7: "Dinner",
	8: "Event",
	9: "Experience",
	10: "Family",
	11: "Fine Dining",
	12: "Italian",
	13: "Lunch",
	14: "River View",
	15: "Street Food",
	16: "Traditional",
	17: "Vietnamese",
}
districts: dict[int, str] = {
	1: "District 1",
	2: "District 2",
	3: "District 3",
	4: "District 4",
	5: "District 5",
	6: "District 6",
	7: "District 7",
	8: "District 8",
	9: "District 9",
	10: "District 10",
	11: "District 11",
	12: "Binh Thanh District",
	13: "Tan Binh District",
	14: "Tan Phu District",
	15: "Go Vap District",
	16: "Phu Nhuan District",
	17: "Binh Tan District",
	18: "Thu Duc City",
	19: "Binh Chanh District",
	20: "Hoc Mon District",
	21: "Cu Chi District",
	22: "Can Gio District",
	23: "Nha Be District",
}


def get_categories_by_ids(list_categories_ids: list[int]) -> list[str]:
	list_categories: list[str] = []
	for category_id in list_categories_ids:
		name = categories.get(category_id)
		if name is not None:
			list_categories.append(name)
	return list_categories


def get_district_by_id(district_id: int) -> str:
	return districts.get(district_id)


def from_entity_to_model(entity: RestaurantEntity) -> RestaurantModel:
	categories = get_categories_by_ids(entity.categories)
	district = get_district_by_id(entity.district)
	restaurant = RestaurantModel(restaurantId=entity.restaurant_id, name=entity.name, address=entity.address,
	                             picture=entity.image, rating=entity.rating, openTime=entity.openTime,
	                             closeTime=entity.closeTime,
	                             district=district,
	                             categories=categories)
	return restaurant
