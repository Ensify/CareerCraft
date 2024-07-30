from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/landing")
@login_required
def landing():
    return render_template('landing.html')


@main.route("/quiz")
def quiz():
    return render_template('quiz.html')