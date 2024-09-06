from firebase_admin import credentials, firestore, initialize_app
from pathlib import Path

cred = credentials.Certificate(Path('pfe-gaming-60db4-firebase-adminsdk-q1p8j-f04d11623b.json'))
initialize_app(cred)

db = firestore.client()
