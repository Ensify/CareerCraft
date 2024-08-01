from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.mongo import MongoHandle
import time
import os
from datetime import datetime
from app.utils.recommend import Recommender

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
    recommender = Recommender()
    user = recommender.mongo.get_user_object(current_user.mongo_objectId)
    recommended_projects = recommender.getRecommendations(user, 1)
    print(recommended_projects)
    return render_template('landing.html', projects=projects, skills=skills_set, roles=roles, recommended_projects = recommended_projects)

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

def get_overall_leaderboard():
    users_data = mongo_handle.get_all_users()

    leaderboard = []

    for user in users_data:
        user_id = user['_id']
        user_enrollments = mongo_handle.get_user_projects(user_id)
        print(user_enrollments)
        total_projects = len(user_enrollments)
        completed_projects = 0
        total_completion_percentage = 0
        earliest_completion_date = None
        
        for enrollment in user_enrollments:
            enroll_id = enrollment['_id']
            user_roadmap = mongo_handle.get_roadmap_object(enroll_id)
            
            if user_roadmap:
                completion_percentage = mongo_handle.get_completion_rate(user_roadmap.get("_id"))

                if completion_percentage == 100:
                    completed_projects += 1
                    completion_dates = mongo_handle.get_updated_dates(user_roadmap["_id"])
                    if completion_dates:
                        project_completion_date = min(completion_dates)
                        if earliest_completion_date is None or project_completion_date < earliest_completion_date:
                            earliest_completion_date = project_completion_date
                total_completion_percentage+=completion_percentage

        avg_completion_percentage = total_completion_percentage / total_projects if total_projects > 0 else 0
        leaderboard.append({
            'userName': user['username'],
            'userRole': user.get('role'),
            'totalProjects': total_projects,
            'completedProjects': completed_projects,
            'avgCompletionPercentage': avg_completion_percentage,
            'earliestCompletionDate': datetime.fromtimestamp(earliest_completion_date).strftime('%Y-%m-%d %H:%M:%S') if earliest_completion_date else 'N/A'
        })
    
    # Sort leaderboard by completed projects, then by avg completion percentage
    leaderboard = sorted(leaderboard, key=lambda x: (x['completedProjects'], x['avgCompletionPercentage'], x['totalProjects']), reverse=True)
    
    return leaderboard



@main.route('/landing/leaderboard')
@login_required
def overall_leaderboard():
  # TODO: To get all the projects, filter tasks using enroll id(roadmap id) and add their completion rates to decide.
    leaderboard = get_overall_leaderboard()
    return render_template('leaderboard.html', overall_leaderboard_sorted=leaderboard)
  