from app import mongo
from bson.objectid import ObjectId
import datetime

class Score:
    @staticmethod
    def upsert_score(user_id, score):

        # Check if user_id is a valid ObjectId, if not, convert it
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user_id")

        user_id_obj = ObjectId(user_id)
        
        # Use findOneAndUpdate for atomic update and retrieval
        current_time = datetime.datetime.utcnow()
        updated_score = mongo.db.scores.find_one_and_update(
            {"user_id": user_id_obj},
            {
                "$inc": {"score": score},
                "$set": {"updated_at": current_time},
                "$setOnInsert": {"created_at": current_time}
            },
            upsert=True,
            return_document=True  # Return the updated document
        )

        # Convert ObjectId to string for the response
        updated_score["_id"] = str(updated_score["_id"])
        updated_score["user_id"] = str(updated_score["user_id"])

        # Return the score data
        return updated_score
    
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