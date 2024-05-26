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
