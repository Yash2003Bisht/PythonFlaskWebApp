"""Performing CRUD operations"""

from flask import Blueprint, abort, flash, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from website.models import UserNotes
from . import db
import jwt
from website import app


views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    token = jwt.encode(
        {
            "First Name": current_user.fname,
            "Last Name": current_user.lname, 
            "Email": current_user.email, 
            "IsActive": True, 
            "Roles": current_user.roles, 
        }
        , app.config["SECRET_KEY"])
    return render_template("home.html", user=current_user, data=jwt.decode(token, app.config["SECRET_KEY"]))

@views.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        if len(title) < 4:
            flash("Your title is too short.", category="danger")
        elif len(description) < 10:
            flash("Your description is too short.", category="danger")
        else:
            note = UserNotes(title=title, description=description, refrence_key=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash("Note added successfully.", category="success")
            return redirect(url_for("views.getall"))
    return render_template("create.html", user=current_user)

@views.route("/delete/<int:user_id>")
@login_required
def delete(user_id):
    note = UserNotes().query.filter_by(id=user_id).first()
    if current_user.id == note.refrence_key or current_user.roles == "Admin":
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully.", category="success")
        return redirect(url_for('views.getall'))
    else:
        abort(401)

@views.route("/put/<int:user_id>", methods=['GET', 'POST'])
@login_required
def put(user_id):
    note = UserNotes().query.filter_by(id=user_id).first()
    if current_user.id == note.refrence_key or current_user.roles == "Admin":
        if request.method == 'POST':
            note.title = request.form['title']
            note.description = request.form['desc']
            note.refrence_key = note.refrence_key
            db.session.commit()
            flash("Note updated successfully.", category="success")
            return redirect(url_for('views.getall'))
        return render_template('put.html', note=note, user=current_user)
    else:
        abort(401)


@views.route("/getall")
@login_required
def getall():
    return render_template("getall.html", user=current_user)

@views.route("/get/<int:id>", methods=['GET', 'POST'])
@login_required
def get(id):
    note = UserNotes().query.filter_by(id=id).first()
    if current_user.id == note.refrence_key or current_user.roles == "Admin":
        return render_template("getonenote.html", note=note, user=current_user)
    else:
        abort(401)

@views.errorhandler(401)
@login_required
def page_not_found(e):
    """showing 401 error if user try to access other user notes. Only admin can access other user note."""
    return render_template('401.html', user=current_user)

