from typing import Any, Callable, Dict, Optional

import requests
from flask import flash, Flask, redirect, render_template, request, Response as FlaskResponse, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkeydelamortquitueavoirsionlachangeunjour'

API_URL = 'http://backend:8000'


def is_logged_in() -> bool:
    return 'id_token' in session


def make_api_request(
        endpoint: str, method: str = 'GET', headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None
) -> Optional[requests.Response]:
    url = f"{API_URL}{endpoint}"
    if headers is None:
        headers = {}

    try:
        if method == 'POST':
            response = requests.post(url, headers=headers, json=json)
        elif method == 'GET':
            response = requests.get(url, headers=headers)
        return response
    except requests.RequestException:
        flash("Failed to connect to the server.", "danger")
        return None


def handle_response(
        response: Optional[requests.Response],
        success_message: Optional[str],
        redirect_target: str,
        error_message: str = 'Action failed',
        success_action: Optional[Callable[[requests.Response], FlaskResponse]] = None
) -> FlaskResponse:
    if response and response.status_code == 200:
        if success_message:
            flash(success_message, "success")
        if success_action:
            return success_action(response)
        return redirect(url_for(redirect_target))
    else:
        error = response.json().get('detail', error_message) if response else error_message
        flash(error, "danger")
        return redirect(url_for(redirect_target))


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
