import os
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine service key path (secret file > env var > default)
secret_file_path = '/etc/secrets/secret_key.txt'
if os.path.exists(secret_file_path):
    with open(secret_file_path) as f:
        SERVICE_KEY_PATH = f.read().strip()
else:
    SERVICE_KEY_PATH = getattr(settings, "SERVICE_KEY_PATH", "serviceAccountKey.json")

# Join with BASE_DIR if it's a relative path
if not os.path.isabs(SERVICE_KEY_PATH):
    SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, SERVICE_KEY_PATH)
else:
    SERVICE_ACCOUNT_PATH = SERVICE_KEY_PATH

# Initialize Firebase with the credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})

bucket = storage.bucket()
