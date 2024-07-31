#load env

import os
from dotenv import load_dotenv
load_dotenv()

# Import necessary libraries

from pymongo import MongoClient

# Set up MongoDB connection

MONGO_URI = os.environ.get('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client['careercraftDB']

project_collection = db["projectsData"]

projects = project_collection.find({})

roles = set()
skills = set()

for project in projects:
    for role in project["roles"]:
        roles.add(role.strip())
    for skill in project["skills"]:
        skills.add(skill.strip())

#save roles and skills in text file sorted 

with open("data/rolesDB.txt", "w") as f:
    for role in sorted(roles):
        f.write(f"{role}\n")

with open("data/skillsDB.txt", "w") as f:
    for skill in sorted(skills):
        f.write(f"{skill}\n")