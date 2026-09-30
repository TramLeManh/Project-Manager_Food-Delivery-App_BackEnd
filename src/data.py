from pymongo import MongoClient
from datetime import time
import uuid

# MongoDB connection
MONGO_DATABASE: str = "pm_project"
MONGO_USERNAME: str = "root"
MONGO_PASSWORD: str = "12345678"
MONGO_HOSTNAME: str = "app.lemanh0902.id.vn"  # The address of your MongoDB server
MONGO_PORT: int = 27017
MONGO_URI: str = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"
client = MongoClient(MONGO_URI)  # Adjust connection string as needed
db = client[MONGO_DATABASE]  # Replace with your database name
collection = db['restaurants']

# Sample data for 3 restaurants
owner_id = str(uuid.uuid4())
restaurants_data = [
	{
		"_id": str(uuid.uuid4()),
		"name": "Pho Saigon",
		"owner_id": owner_id,
		"address": "123 Vietnamese Street, District 1",
		"district": {
			"id": str(uuid.uuid4()),
			"name": "District 1"
		},
		"categories": [
			{
				"id": str(uuid.uuid4()),
				"name": "Vietnamese",
				"image": "https://example.com/images/vietnamese.jpg"
			},
			{
				"id": str(uuid.uuid4()),
				"name": "Noodles",
				"image": "https://example.com/images/noodles.jpg"
			}
		],
		"image": "https://example.com/images/pho_saigon.jpg",
		"picture": "https://example.com/images/pho_saigon_main.jpg",
		"rating": 4.5,
		"openTime": "07:00",
		"closeTime": "22:00",
		"created_at": "15:13"
	},
	{
		"_id": str(uuid.uuid4()),
		"name": "Pizza Corner",

		"owner_id": owner_id,

		"address": "456 Italian Avenue, District 3",
		"district": {
			"id": str(uuid.uuid4()),
			"name": "District 3"
		},
		"categories": [
			{
				"id": str(uuid.uuid4()),
				"name": "Italian",
				"image": "https://example.com/images/italian.jpg"
			},
			{
				"id": str(uuid.uuid4()),
				"name": "Pizza",
				"image": "https://example.com/images/pizza.jpg"
			},
			{
				"id": str(uuid.uuid4()),
				"name": "Fast Food",
				"image": "https://example.com/images/fastfood.jpg"
			}
		],
		"image": "https://example.com/images/pizza_corner.jpg",
		"picture": "https://example.com/images/pizza_corner_main.jpg",
		"rating": 4.2,
		"openTime": "11:00",
		"closeTime": "23:30",
		"created_at": "15:13"
	},
	{
		"_id": str(uuid.uuid4()),
		"name": "Sushi Zen",
		"owner_id": owner_id,
		"address": "789 Japanese Boulevard, District 7",
		"district": {
			"id": str(uuid.uuid4()),
			"name": "District 7"
		},
		"categories": [
			{
				"id": str(uuid.uuid4()),
				"name": "Japanese",
				"image": "https://example.com/images/japanese.jpg"
			},
			{
				"id": str(uuid.uuid4()),
				"name": "Sushi",
				"image": "https://example.com/images/sushi.jpg"
			},
			{
				"id": str(uuid.uuid4()),
				"name": "Seafood",
				"image": "https://example.com/images/seafood.jpg"
			}
		],
		"image": "https://example.com/images/sushi_zen.jpg",
		"picture": "https://example.com/images/sushi_zen_main.jpg",
		"rating": 4.8,
		"openTime": "17:00",
		"closeTime": "01:00",
		"created_at": "15:13"
	}
]

# Insert the data
try:
	result = collection.insert_many(restaurants_data)
	print(f"Successfully inserted {len(result.inserted_ids)} restaurants")
	print("Inserted IDs:", result.inserted_ids)

	# Verify insertion by counting documents
	count = collection.count_documents({})
	print(f"Total documents in collection: {count}")

except Exception as e:
	print(f"Error inserting data: {e}")

# Optional: Display inserted data
print("\nInserted restaurants:")
for restaurant in collection.find():
	print(f"- {restaurant['name']} (ID: {restaurant['_id']})")

# Close connection
client.close()