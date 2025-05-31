import os
import json
import firebase_admin
from firebase_admin import credentials, storage

# Parse the Firebase credentials from the environment variable
firebase_creds_json = os.environ['FIREBASE_CREDENTIALS']
firebase_creds_dict = json.loads(firebase_creds_json)

# Initialize the Firebase app
cred = credentials.Certificate(firebase_creds_dict)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twinbrook-12f84.appspot.com'
})

bucket = storage.bucket()
