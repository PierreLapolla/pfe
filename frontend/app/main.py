import os

import requests
from flask import flash, Flask, redirect, render_template, request, Response as FlaskResponse, session, url_for

from .helpers import handle_response, is_logged_in, make_api_request

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register() -> FlaskResponse:
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        display_name = request.form['display_name']
        response = make_api_request('/register', method='POST', json={
            "email": email,
            "password": password,
            "display_name": display_name
        })
        return handle_response(response, "Registration successful! Please log in.", 'login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login() -> FlaskResponse:
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = make_api_request('/login', method='POST', json={"email": email, "password": password})

        def on_success(response: requests.Response) -> FlaskResponse:
            data = response.json()
            session['id_token'] = data['id_token']
            return redirect(url_for('profile'))

        return handle_response(response, "Logged in successfully!", 'profile', "Login failed",
                               success_action=on_success)
    return render_template('login.html')


@app.route('/profile')
def profile() -> FlaskResponse:
    if not is_logged_in():
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    id_token = session['id_token']
    headers = {"Authorization": f"Bearer {id_token}"}
    response = make_api_request('/profile', headers=headers)

    def on_success(response: requests.Response) -> str:
        profile_data = response.json()
        return render_template('profile.html', profile=profile_data)

    return handle_response(response, None, 'login', "Failed to load profile", success_action=on_success)


@app.route('/logout')
def logout() -> FlaskResponse:
    session.pop('id_token', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))


@app.route('/delete-account', methods=['POST'])
def delete_account() -> FlaskResponse:
    if not is_logged_in():
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    id_token = session['id_token']
    headers = {"Authorization": f"Bearer {id_token}"}
    response = make_api_request('/delete-account', method='POST', headers=headers)
    return handle_response(response, "Account deleted successfully.", 'index', "Failed to delete account")
