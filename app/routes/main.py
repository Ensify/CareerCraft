from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.mongo import MongoHandle
import time
import os


main = Blueprint('main', __name__)
mongo_handle = MongoHandle()

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/landing")
@login_required
def landing():
    projects = mongo_handle.get_all_projects()
    skills_set = []
    print(os.listdir("data"))
    with open(os.path.join("data", "skills.txt")) as f:
        for line in f:
            skills_set.append(line.strip().capitalize())
    roles = []
    with open("data/roles.txt") as f:
        for line in f:
            roles.append(line.strip())
    return render_template('landing.html', projects=projects, skills=skills_set, roles=roles)

@main.route("/project/<int:id>")
@login_required
def get_project_details(id):
    current_project = mongo_handle.get_project_object(id)
    is_enrolled = mongo_handle.is_user_enrolled(current_user.mongo_objectId, id)
    return render_template('project.html', project=current_project, enrolled=is_enrolled is not None,project_id=current_project["projectId"], is_project= True)

@main.route("/enroll", methods=["POST"])
@login_required
def enroll():
    print(request.form)
    project_id = int(request.form.get("projectId"))
    print(f"PROJECT ID: {project_id}")
    date_object = int(time.time() * 1000)
    # formatted_date = date_object.strftime("%d/%m/%Y")
    enroll_data = {
        "userId": current_user.mongo_objectId,
        "projectId": project_id,
        "dateEnrolled": date_object,
        "generateRoadmap": False
    }
    mongo_handle.add_enroll_object(enroll_data)
    return redirect(url_for('main.get_project_details', id=project_id))

@main.route('/landing/leaderboard')
@login_required
def overall_leaderboard(project_id):
  # TODO: To get all the projects, filter tasks using enroll id(roadmap id) and add their completion rates to decide.

  pass