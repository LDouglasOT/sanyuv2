import os
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings



# Get the absolute path to the JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, settings.SERVICE_KEY_PATH)

# Load the Firebase credentials from the file
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})

bucket = storage.bucket()
