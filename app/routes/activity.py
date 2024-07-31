from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.mongo import MongoHandle
from ..utils import roadmap


activity = Blueprint('activity', __name__)
mongo_handle = MongoHandle()


@activity.route("/learning/<int:project_id>")
def learning(project_id):
    roadmap_object = roadmap.get_roadmap(project_id, current_user.mongo_objectId)
    if not roadmap_object:
        flash("User not enrolled in this course. Please report if you think this is a mistake.","error")
        return redirect(url_for('main.landing'))
    return render_template('learning.html', roadmap=roadmap_object, project_id=project_id)


@activity.route("/quiz/<int:project_id>", methods=["GET"])
@login_required
def quiz(project_id):
    quiz_questions = mongo_handle.get_quiz_object(project_id)
    return render_template('quiz.html', quiz_questions=quiz_questions)


@activity.route("/quiz/<int:project_id>", methods=["POST"])
@login_required
def process_quiz(project_id):
    if request.method == "POST":
        quiz_responses = request.form.get('quizResponses')
        if quiz_responses is not None:
            mongo_handle.put_quiz_reponses(current_user.id, project_id, quiz_responses)
            flash("Quiz submitted successfully!", "success")
                        
    return redirect(url_for('activity.learning', project_id=project_id))




@activity.route('/learning/<int:project_id>/leaderboard')
@login_required
def project_leaderboard(project_id):
    # TODO: To get all the projects, filter tasks using enroll id(roadmap id) and add their completion rates to decide.
    pass

