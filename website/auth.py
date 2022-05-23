"""Setting up authorization"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import UserData, db
from flask_login import login_required, login_user, logout_user, current_user
import re

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(password)
        user = UserData.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("login successfully.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="danger")
        else:
            flash("Invalid email.", category="danger")
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    admin = request.args.get("admin")  # return True for admin user
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        if UserData.query.filter_by(email=email).first():
            flash("User already exists", category="danger")
        elif len(fname) < 3:
            flash("First name must be greater than 2 characters.", category="danger")
        elif not bool(re.search(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9]*\.[a-zA-Z]{1,3}$", email)):
            flash("Please type a valid email.", category="danger")
        elif len(password) < 9:
            flash("Your password must be at least 8 characters.", category="danger")
        elif password != confirm_password:
            flash("Password don't match.", category="danger")
        else:
            admin = bool(request.args.get("admin"))
            user_data = UserData(email=email, fname=fname, lname=lname, roles="Admin" if admin == True else "User",password=generate_password_hash(password=password, salt_length=14))
            db.session.add(user_data)
            db.session.commit()
            flash("Account created", category="success")
            login_user(user_data, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign.html", user=current_user, isadmin=admin)

