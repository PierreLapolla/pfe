from pathlib import Path

from firebase_admin import credentials, firestore, initialize_app

from .config_loader import config
from .logger import log


class FirebaseClient:
    """
    Singleton class to initialize and manage the Firebase Firestore client.
    """
    _instance = None

    def __new__(cls) -> firestore.client:
        """
        Create a new instance of FirebaseClient if it doesn't exist.

        :return: The singleton instance of FirebaseClient.
        :rtype: FirebaseClient
        :raises FileNotFoundError: If the Firebase credentials file is not found.
        """
        if cls._instance is None:
            credentials_path = Path(config('FIREBASE_CREDENTIALS_PATH'))
            if not credentials_path.is_file():
                log.critical(f'firebase credentials file not found: {credentials_path}')
                raise FileNotFoundError(f'Firebase credentials file not found: {credentials_path}')

            initialize_app(credentials.Certificate(credentials_path))
            cls._instance = firestore.client()
            log.debug('firebase client initialized')
        return cls._instance


db: firestore.client = FirebaseClient()
