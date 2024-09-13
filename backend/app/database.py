import os
from pathlib import Path
from firebase_admin import credentials, firestore, initialize_app
from .logger import log

class FirebaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            credentials_path = Path(os.getenv('FIREBASE_CREDENTIALS_PATH'))
            if not credentials_path.is_file():
                log.error(f'firebase credentials file not found: {credentials_path}')
                raise FileNotFoundError(f'Firebase credentials file not found: {credentials_path}')

            initialize_app(credentials.Certificate(credentials_path))
            cls._instance = firestore.client()
            log.info('firebase client initialized')
        return cls._instance

db = FirebaseClient()
