# main.py

import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, flash
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise Exception("SECRET_KEY is not set in environment variables")

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
            session['refresh_token'] = data['refresh_token']
            flash("Logged in successfully!", "success")
            return redirect(url_for('profile'))
        else:
            error = response.json().get('detail', 'Login failed')
            flash(error, "danger")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/profile')
def profile():
    id_token = session.get('id_token')
    if not id_token:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))
    headers = {'Authorization': f'Bearer {id_token}'}
    response = requests.get(f"{API_URL}/profile", headers=headers)
    if response.status_code == 200:
        user_profile = response.json()
        return render_template('profile.html', user=user_profile)
    elif response.status_code == 401:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for('login'))
    else:
        error = response.json().get('detail', 'Failed to fetch profile')
        flash(error, "danger")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))
