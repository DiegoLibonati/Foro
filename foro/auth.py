import re
from flask import Blueprint, render_template,request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .functions import get_time_login

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET' ,'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_db = User.query.filter_by(username=username).first()
        
        if user_db:
            if check_password_hash(user_db.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user_db, remember=True)

                user_db.last_connection = get_time_login()
                db.session.commit()

                return redirect(url_for('views.home'))
            else:
                flash("Invalid password", category="error")
        else:
            flash("Invalid username", category="error")

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login', user=current_user))

@auth.route('/sign-up', methods=['GET' ,'POST'])
def sign_up():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password") 

    user_db = User.query.filter_by(username=username).first()
    email_db = User.query.filter_by(email=email).first()

    if user_db:
        flash("The user already exists", category="error")
    elif email_db:
        flash("The email already exists", category="error")
    elif not password == confirm_password:
        flash("Passwords do not match", category="error")
    elif (not username or not email or not password or not confirm_password) or (username.isspace() or email.isspace() or password.isspace() or confirm_password.isspace()):
        flash("Blank spaces or spaces at the end or beginning are not allowed.", category="error")
    elif len(username) <= 2:
        flash("The username must be longer than 2 characters.", category="error")
    elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        flash("Invalid email.", category="error")
    elif len(password) <= 5:
        flash("The password must be longer than 5 characters.", category="error")
    else: 
        new_user = User(username = username, email = email, password = generate_password_hash(password), last_connection = get_time_login())
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)