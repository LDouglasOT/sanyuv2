import os
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Priority: /etc/secrets/secret_key.txt > Django settings > fallback
secret_file_path = '/etc/secrets/secret_key.txt'

if os.path.exists(secret_file_path):
    with open(secret_file_path) as f:
        SERVICE_ACCOUNT_PATH = f.read().strip()
else:
    # Try to load from settings, fallback to 'serviceAccountKey.json'
    SERVICE_ACCOUNT_PATH = getattr(settings, "SERVICE_KEY_PATH", "serviceAccountKey.json")

# If it's a relative path, make it absolute from BASE_DIR
if not os.path.isabs(SERVICE_ACCOUNT_PATH):
    SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, SERVICE_ACCOUNT_PATH)

# Check if the file exists before proceeding
if not os.path.exists(SERVICE_ACCOUNT_PATH):
    raise FileNotFoundError(f"Firebase service account key not found at: {SERVICE_ACCOUNT_PATH}")

# Initialize Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})

bucket = storage.bucket()
