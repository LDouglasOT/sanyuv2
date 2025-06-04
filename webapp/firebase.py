import os
import requests
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

SERVICE_ACCOUNT_URL = os.environ.get("SERVICE_ACCOUNT_URL")

response = requests.get(SERVICE_ACCOUNT_URL)
with open(KEY_PATH, "wb") as f:
    f.write(response.content)

cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})
bucket = storage.bucket()
