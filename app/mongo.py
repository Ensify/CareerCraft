from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
from app.models import User

class MongoHandle:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['careercraftDB']
        self.user_collection = self.db['userData']

    def get_user_object(self, user_id):
        user = User.query.get(int(user_id))
        if user:
            mongo_id = user.mongo_objectId
            user_dict = self.user_collection.find_one({'_id': ObjectId(mongo_id)})
            return user_dict
        return None

    def add_user_object(self, user_data):
        result = self.user_collection.insert_one(user_data)
        return str(result.inserted_id)
