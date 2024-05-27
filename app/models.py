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
    

class Score:
    @staticmethod
    def upsert_score(user_id, score):

        # Check if user_id is a valid ObjectId, if not, convert it
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user_id")

        user_id_obj = ObjectId(user_id)

        # Find the existing score document for the user
        existing_score = mongo.db.scores.find_one({"user_id": user_id_obj})

        if existing_score:
            # User exists, update the score
            new_score = existing_score["score"] + score
            mongo.db.scores.update_one(
                {"user_id": user_id_obj},
                {"$set": {"score": new_score, "updated_at": datetime.datetime.utcnow()}}
            )
            existing_score["score"] = new_score
            existing_score["updated_at"] = datetime.datetime.utcnow()
            score_data = existing_score
        else:
            # User does not exist, create a new score document
            score_data = {
                "user_id": user_id_obj,
                "score": score,
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow()
            }
            result = mongo.db.scores.insert_one(score_data)
            score_data["_id"] = str(result.inserted_id)

        # Convert ObjectId to string for the response
        score_data["_id"] = str(score_data["_id"])
        score_data["user_id"] = str(score_data["user_id"])

        # Return the score data
        return score_data
    
    @staticmethod
    def calculate_winner():
        pipeline = [
            {"$sort": {"score": -1}},  # Sort by score in descending order
            {"$limit": 2},  # Limit to the top document
            {"$project": {"user_id": 1, "score": 1}}  # Project only necessary fields
        ]

        highest_score_users = list(mongo.db.scores.aggregate(pipeline))

        # Check if any users have a score
        if highest_score_users:

            # Get the highest score
            highest_score = highest_score_users[0]["score"]
            
            # Filter users with the highest score
            top_users = [user for user in highest_score_users if user["score"] == highest_score]

            if len(top_users) == 1:

                winner = {
                    "user_id": str(top_users[0]["user_id"]),
                    "score": top_users[0]["score"],
                    "created_at": datetime.datetime.utcnow()
                }

                # Store the winner in the winners collection
                winners_collection = mongo.db.winners
                result = winners_collection.insert_one(winner)
                winner["_id"] = str(result.inserted_id)
                return winner
            else:
                # If there's a tie, return a message indicating no winner
                return None
        else:
            # No users found
            return None