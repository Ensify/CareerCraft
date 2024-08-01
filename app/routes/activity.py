import json
from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.mongo import MongoHandle
from app.utils import claude


activity = Blueprint('activity', __name__)
mongo_handle = MongoHandle()


@activity.route("/learning/<int:project_id>")
def learning(project_id):

    enroll_object = mongo_handle.is_user_enrolled(current_user.mongo_objectId, project_id)

    if not enroll_object:
        flash("User not enrolled in this course. Please report if you think this is a mistake.","error")
        return redirect(url_for('main.landing'))
    
    roadmap_object = mongo_handle.get_roadmap_object(enroll_object["_id"])
    progress_data = mongo_handle.get_progress(roadmap_object["_id"])

    roadmap = roadmap_object["roadmap"]
    if roadmap:
        roadmap = roadmap.get("intermediate goals")    

    return render_template('learning.html', roadmap_object = roadmap, project_id = project_id, progress_data = progress_data)


@activity.route("/quiz/<int:project_id>", methods=["GET"])
@login_required
def quiz(project_id):
    #Validate Quiz
    #TODO: Check if user is enrolled in project and not already taken quiz and exit route

    quiz_questions = mongo_handle.get_quiz_object(project_id)["skills"]
    return render_template('quiz.html', data=quiz_questions, project_id = project_id, is_project= True)


@activity.route("/quiz/<int:project_id>", methods=["POST"])
@login_required
def process_quiz(project_id):

    results = request.data.decode("utf-8")
    quiz_responses = json.loads(results)
    print(quiz_responses)

    if quiz_responses:
        
        mongo_handle.put_quiz_reponses(current_user.mongo_objectId, project_id, quiz_responses)
        description = mongo_handle.get_project_object(project_id)["description"]
        skillslevels = []
        for skill in quiz_responses:
            skillslevels.append((skill["skill"], skill["mark"]))

        roadmap = claude.generate_roadmap(description, skillslevels)

        if roadmap:
            enroll_object = mongo_handle.is_user_enrolled(current_user.mongo_objectId, project_id)
            mongo_handle.put_roadmap_object(roadmap, enroll_object["_id"])
            mongo_handle.set_generated_roadmap(enroll_object)

        flash("Quiz submitted successfully!", "success")
                        
    return {"redirect":url_for('activity.learning', project_id=project_id, is_project= True)}




@activity.route('/learning/<int:project_id>/leaderboard')
@login_required
def project_leaderboard(project_id):
    # TODO: To get all the projects, filter tasks using enroll id(roadmap id) and add their completion rates to decide.
    enrollments = mongo_handle.get_project_enrollments(project_id)
    leaderboard = []
    project_name = mongo_handle.get_project_object(project_id)["title"]
    for enroll in enrollments:
        roadmap_obj = mongo_handle.get_roadmap_from_enrollment(enroll["_id"])
        user =  mongo_handle.get_user_object(enroll["userId"])
        print("User: ", enroll["userId"])
        if roadmap_obj:
            completion_rate = mongo_handle.get_completion_rate(roadmap_obj["_id"])
        else:
            completion_rate = 0 
        leaderboard.append({
            "userName": user["username"],
            "userRole": user.get("role"),
            "enrollDate": enroll["dateEnrolled"],
            "completionPercentage": completion_rate
        })
    leaderboard.sort(key=lambda x: [x["completionPercentage"], -x["enrollDate"]], reverse=True)
    return render_template("leaderboard.html", leaderboard_sorted=leaderboard, project_name=project_name)


