from typing import Any
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
from app.models import User
import time

class MongoHandle:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['careercraftDB']
        self.user_collection = self.db['userData']
        self.project_collection = self.db['projectsData']
        self.enroll_collection = self.db['enrollData']
        self.quiz_collection = self.db['quizData']
        self.quiz_responses_collection = self.db['quizResponsesData']
        self.roadmap_collection = self.db['roadmapData']
        self.progress_collection = self.db['progressData']

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

    def get_all_projects(self):
        projects = self.project_collection.find()
        return [project for project in projects]
    
    def add_project_object(self, project_data):
        result = self.project_collection.insert_one(project_data)
        return str(result.inserted_id)
    
    def get_project_object(self, project_id):
        project = self.project_collection.find_one({'projectId': project_id})
        return project
    
    def add_enroll_object(self, enroll_data):
        result = self.enroll_collection.insert_one(enroll_data)
        return str(result.inserted_id)
    
    def is_user_enrolled(self, user_id, project_id):
        enroll = self.enroll_collection.find_one({'userId': user_id, 'projectId': project_id})
        return enroll
    
    def get_user_enrollments(self, user_id):
        enrollments = self.enroll_collection.find({'userId': user_id["_id"]})
        return [enroll for enroll in enrollments]
    

    def get_quiz_object(self, project_id):
        quiz = self.quiz_collection.find_one({'projectId': project_id})
        if quiz:
            return quiz
        return None
    
    def put_quiz_reponses(self, user_id, project_id, responses):
        enroll = self.is_user_enrolled(user_id, project_id)
        if enroll:
            quiz_responses = self.quiz_responses_collection.find_one({'enrollId': enroll["_id"]})
            if quiz_responses:
                self.quiz_responses_collection.update_one(
                    {'enrollId': enroll["_id"]},
                    {'$set': {'quizResponses': responses}}
                )
            else:
                self.quiz_responses_collection.insert_one({
                    'enrollId': enroll["_id"],
                    'quizResponses': responses
                })

            return True
        return False
    
    def get_quiz_responses(self, enroll_id):
        quiz_responses = self.quiz_responses_collection.find_one({'enrollId': enroll_id})
        if quiz_responses:
            return quiz_responses['quizResponses']
        return None

    def update_enroll_object(self, project_id, user_id):
        enroll = self.is_user_enrolled(user_id, project_id)
        if enroll:
            self.enroll_collection.update_one(
                {'_id': enroll["_id"]},
                {'$set': {'generateRoadmap': True}}
            )
            return True
        return False
    def set_generated_roadmap(self,enroll_object):
        self.enroll_collection.update_one(
            {'_id': enroll_object["_id"]},
            {'$set': {'generateRoadmap': True}}
        )
        return True

    def put_roadmap_object(self, roadmap, enroll_id):
        result = self.roadmap_collection.insert_one({
            'enrollId': enroll_id,
            'roadmap': roadmap
        })
        insert_id = str(result.inserted_id)
        today = int(time.time() * 1000)
        activities = []
        intermediate_goals = roadmap["intermediate goals"]

        for goalIdx, goal in enumerate(intermediate_goals):
            for milestoneIdx, milestone in enumerate(goal["milestones"]):
                for taskIdx, task in enumerate(milestone["tasks"]):
                    activities.append({
                        "roadmapId": insert_id,
                        "taskId": str(goalIdx+1)+"-"+str(milestoneIdx+1)+"-"+str(taskIdx+1),
                        "completion": 0,
                        "dateCreated": today,
                        "dateUpdated": today
                    })
                    
        self.progress_collection.insert_many(activities)
        return insert_id
    
    def get_roadmap_object(self, enroll_id):
        roadmap = self.roadmap_collection.find_one({'enrollId': enroll_id})
        if roadmap:
            return roadmap
        return None
    
    def get_user_projects(self, user_id):
        result = self.enroll_collection.find({'userId': user_id})

        return [res for res in result]
    def update_user_profile(self, user_id, linkedin, github, role, skills):
        user_obj = self.get_user_object(user_id)
        result = self.user_collection.update_one(filter={'_id': user_obj["_id"]}, update={'$set': {'linkedin': linkedin, 'github': github, 'role':role, 'skills': skills}})
        return result.modified_count
    
    def get_project_enrollments(self, project_id):
        enrollments = self.enroll_collection.find({'projectId': project_id})
        return [enroll for enroll in enrollments]
    
    def get_progress(self, roadmapId):
        roadmapId = str(roadmapId)
        tasks = self.progress_collection.find({'roadmapId': roadmapId})
        progress_data = {}
        for task in tasks:
            progress_data[task['taskId']] = task['completion']
        return progress_data