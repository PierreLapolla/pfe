import os
from typing import Any, Callable, Dict, Optional

import requests
from flask import flash, FlaskResponse, redirect, session, url_for


def is_logged_in() -> bool:
    return 'id_token' in session


def make_api_request(
        endpoint: str, method: str = 'GET', headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None
) -> Optional[requests.Response]:
    url = f"{os.getenv('API_URL')}{endpoint}"
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
