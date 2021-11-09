from typing import MutableSet
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.json.tag import PassDict
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist", category="error")

    return  render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if not checkForAdmin():
        createAdmin()
        return redirect(url_for("views.home"))
    def check_password(password):
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) and any(x.isdigit() for x in password) and (len(password) >= 6)):
            return True
        else:
            return False

    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists!", category="error")
        elif len(email) < 4:
            flash("Email must be more than 4 characters long!", category="error")
        elif len(first_name) < 2:
            flash("Your first name must be more than 2 characters long!", category="error")
        elif password1 != password2:
            flash("Your passwords do not match!", category="error")
        elif not(check_password(password1)):
            flash("Your password must contain at least 1 capital letter, one lowercase letter, one digit and it must be bigger than 6 characters long!", category="error")
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name.capitalize(), password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    
    
    
    return render_template("sign_up.html", user=current_user)


@auth.route("/", methods=["GET", "POST"])
def mainHome():
    return render_template("main-home.html", user=current_user)




def createAdmin():

    def checkForAdmin():
        adminUser = User.query.filter_by(email="admin@gmail.com").first()
        if adminUser:
            return True
        else:
            return False


    if not checkForAdmin():
        new_admin_user = User(email="admin@gmail.com", first_name="Admin", password=generate_password_hash("MainAdmin", method="sha256"), admin=True)
        db.session.add(new_admin_user)            
        db.session.commit()
        login_user(new_admin_user, remember=True)
        print("Admin Account Created")
        flash("Admin Account created!", category="success")
    



def checkForAdmin():
        adminUser = User.query.filter_by(email="admin@gmail.com").first()
        if adminUser:
            return True
        else:
            return False