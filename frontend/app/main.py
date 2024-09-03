import requests
from flask import flash, Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkeydelamortquitueavoirsionlachangeunjour'

API_URL = 'http://backend:8000'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        display_name = request.form['display_name']
        response = requests.post(f"{API_URL}/register", json={
            "email": email,
            "password": password,
            "display_name": display_name
        })
        if response.status_code == 200:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        else:
            error = response.json().get('detail', 'Registration failed')
            flash(error, "danger")
            return render_template('register.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            session['id_token'] = data['id_token']
            flash("Logged in successfully!", "success")
            return redirect(url_for('profile'))
        else:
            error = response.json().get('detail', 'Login failed')
            flash(error, "danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'id_token' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    id_token = session['id_token']
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.get(f"{API_URL}/profile", headers=headers)

    if response.status_code == 200:
        profile_data = response.json()
        return render_template('profile.html', profile=profile_data)
    else:
        flash("Failed to load profile.", "danger")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('id_token', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))
