from app import mongo
from bson.objectid import ObjectId
import datetime
from faker import Faker

fake = Faker()

class User:
    @staticmethod
    def create_user():
        user = {
            "name": fake.name(),
            "age": fake.random_int(min=18, max=80),
            "address": fake.address(),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user)
        user["_id"] = str(result.inserted_id)
        return user

    @staticmethod
    def delete_user(user_id):
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @staticmethod
    def get_all_users(page=1, page_size=20):
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20

        pipeline = [
            {
                "$lookup": {
                    "from": "scores",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "scores"
                }
            },
            {
                "$addFields": {
                    "score": { "$ifNull": [ { "$arrayElemAt": ["$scores.score", 0] }, 0 ] }
                }
            },
            {
                "$project": {
                    "scores": 0  # Exclude the 'scores' array from the results
                }
            },
            {
                "$sort": {"score": -1}  # Sort users by score in descending order
            },
            {
                "$skip": (page - 1) * page_size
            },
            {
                "$limit": page_size
            }
        ]

        users = list(mongo.db.users.aggregate(pipeline))
        for user in users:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string

        return users
    
    @staticmethod
    def get_users_grouped_by_score():
        pipeline = [
            {
                "$lookup": {
                    "from": "scores",
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "score_data"
                }
            },
            {
                "$unwind": "$score_data"
            },
            {
                "$group": {
                    "_id": "$score_data.score",
                    "names": {"$push": "$name"},
                    "average_age": {"$avg": "$age"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "score": "$_id",
                    "names": 1,
                    "average_age": {"$round": ["$average_age", 2]}
                }
            },
            {
                "$sort": {"score": 1}
            }
        ]

        result = list(mongo.db.users.aggregate(pipeline))

        # Transform result to the desired JSON format
        output = {}
        for item in result:
            score = str(item["score"])
            output[score] = {
                "names": item["names"],
                "average_age": item["average_age"]
            }
        return output