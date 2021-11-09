from flask import Blueprint, render_template, request, flash, jsonify
from flask.json import jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note
from website import db
import json

views = Blueprint('views', __name__)



@views.route('/notes', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.admin:
        print("This is an admin user!")
        return render_template("admin.html", user=current_user)
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("notes.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.admin:
        print("This is an admin area going to!")
        return render_template("admin.html", user=current_user)