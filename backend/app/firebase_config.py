from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

load_dotenv()

cred = credentials.Certificate(Path('pfe-gaming-firebase-adminsdk-3n7rw-15c59651df.json'))
firebase_admin.initialize_app(cred)

db = firestore.client()
