from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from app.mongo import MongoHandle
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)
mongoHandle = MongoHandle()

@auth.route("/")
@auth.route("/auth", methods=['GET', 'POST'])
def authenticate():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        form_type = request.form.get('form-type')
        
        if form_type == 'login':
            email = request.form.get('login-email')
            password = request.form.get('login-password')
            
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                flash("Logged in successfully", 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            
            else:
                flash('Login Unsuccessful. Please check email and password', 'error')
        
        elif form_type == 'register':
            username = request.form.get('register-username')
            email = request.form.get('register-email')
            password = request.form.get('register-password')
            confirm_password = request.form.get('register-confirm-password')
            
            if password != confirm_password:
                flash('Passwords do not match!', 'error')
            elif User.query.filter_by(username=username).first():
                flash('That username is taken. Please choose a different one.', 'error')
            elif User.query.filter_by(email=email).first():
                flash('This email address is already registered. Please login instead.', 'error')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user_data = {
                    'email': email,
                    'username': username,
                }
                mongo_object_id = mongoHandle.add_user_object(user_data)
                
                user = User(
                    username=username,
                    email=email,
                    password=hashed_password,
                    mongo_objectId=mongo_object_id
                )
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('auth.authenticate'))

    return render_template('auth.html')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route("/profile")
@login_required
def profile():
    user = User.query.get(current_user.id)
    return render_template('profile.html', user=user)
