# import json
import firebase_admin
from firebase_admin import db, credentials

# Path to the JSON file
# file_path = 'firebase_config.json'

# Open and load the JSON file
# with open(file_path, 'r') as file:
    # firebase_config = json.load(file)

firebase_credentials = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(firebase_credentials)
