import os
from pathlib import Path

from firebase_admin import credentials, firestore, initialize_app

credentials_path = Path(os.getenv('FIREBASE_CREDENTIALS_PATH'))
if not credentials_path.is_file():
    raise FileNotFoundError(f'Firebase credentials file not found: {credentials_path}')

initialize_app(credentials.Certificate(credentials_path))

db = firestore.client()
