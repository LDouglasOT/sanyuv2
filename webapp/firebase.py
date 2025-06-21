import os
import requests
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

SERVICE_ACCOUNT_URL = "https://firebasestorage.googleapis.com/v0/b/twinbrook-12f84.appspot.com/o/twinbrook-12f84-firebase-adminsdk-la9vk-02f288b2ba.json?alt=media&token=2abc1b23-5322-428f-ac9b-6fa9ac09b0b2"

response = requests.get(SERVICE_ACCOUNT_URL)
with open(KEY_PATH, "wb") as f:
    f.write(response.content)

cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})
bucket = storage.bucket()
