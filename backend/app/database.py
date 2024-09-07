import os
from pathlib import Path

from firebase_admin import credentials, firestore, initialize_app

credentials_path = Path(os.getenv('FIREBASE_CREDENTIALS_PATH'))
cred = credentials.Certificate(credentials_path)
initialize_app(cred)

db = firestore.client()
