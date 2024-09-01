import requests
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

from . import login_manager  # Ensure this import is correct


# Define your forms directly in routes.py
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


main_blueprint = Blueprint("main", __name__)

API_BASE_URL = "http://backend:80"


class User(UserMixin):
    def __init__(self, uid, email):
        self.id = uid
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f"{API_BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        return User(uid=user_data['uid'], email=user_data['email'])
    return None


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {"email": form.email.data, "password": form.password.data}
        response = requests.post(f"{API_BASE_URL}/login", json=data)
        if response.status_code == 200:
            user_data = response.json()
            user = User(uid=user_data['uid'], email=user_data['email'])
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Login failed. Check your credentials.", "danger")
    return render_template("login.html", form=form)


@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {"email": form.email.data, "password": form.password.data}
        response = requests.post(f"{API_BASE_URL}/register", json=data)
        if response.status_code == 201:
            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("main.login"))
        else:
            flash("Registration failed. Try again.", "danger")
    return render_template("register.html", form=form)


@main_blueprint.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
