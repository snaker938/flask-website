from flask import Blueprint, render_template, request, flash, jsonify
from flask.json import jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note, User
from website import db
import json
from werkzeug.security import check_password_hash

views = Blueprint('views', __name__)



@views.route('/notes', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.admin:
        pass
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    if not current_user.admin:
        return render_template("notes.html", user=current_user)
    else:
        defaultAdmin = checkAdminDefaultPassword()
        return render_template("admin-home.html", user=current_user, defaultAdmin=defaultAdmin)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        elif current_user.admin:
            print("Forcefully deleting note..")
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.admin:
        print("Going to admin area")
        defaultAdmin = checkAdminDefaultPassword()
        return render_template("admin-home.html", user=current_user, defaultAdmin=defaultAdmin)
    else:
        return render_template("notes.html", user=current_user)
    
    
    
@views.route('/admin/all-users', methods=['GET', 'POST'])
@login_required
def all_users():
    if current_user.admin:
        if request.method == 'POST':
            if list(request.form.keys())[0] == 'view':
                mock_user_id = request.form['view']
                mock_user = User.query.get(mock_user_id)
                return render_template("mock-user.html", user=current_user, mock_user=mock_user)
        users = find_data()
        return render_template("all-users.html", user=current_user, all_users=users)
    else:
        return render_template("notes.html", user=current_user)
    
    
    
def checkAdminDefaultPassword():
    if check_password_hash(current_user.password, "MainAdmin"):
        return True
    
    

def find_data():
    users = User.query.all()
    return users
