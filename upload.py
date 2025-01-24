import json
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "leetcode"
COLLECTION_NAME = "problems"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]



# Path to your JSON file
json_file_path = "data\data.json"  # Replace with the actual file path

collection.update_many({}, {"$set": {"done": False}})

print("Done field added to all documents.")

# Load JSON data from the file
# try:
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)  # Assumes the JSON file contains an array of objects
# except Exception as e:
#     print(f"Error reading JSON file: {e}")
#     exit()

# # Insert data into MongoDB
# try:
#     if isinstance(data, list):
#         collection.insert_many(data)
#         print(f"Inserted {len(data)} documents into the collection.")
#     elif isinstance(data, dict):
#         collection.insert_one(data)
#         print("Inserted one document into the collection.")
#     else:
#         print("Invalid JSON format. Expected a list or dictionary.")
# except Exception as e:
#     print(f"Error inserting data into MongoDB: {e}")
#     exit()

# Close the MongoDB connection
client.close()
