from google.cloud import storage
from firebase_admin import credentials, initialize_app, storage as firebase_storage

def get_firebase_bucket():
    cred = credentials.Certificate("/Users/soyun/Documents/Projects/Server/firebase_settings.json")
    app = initialize_app(cred, {'storageBucket': 'bigsogo-806df.appspot.com'})
    bucket = firebase_storage.bucket(app=app)
    return bucket

def get_bucket() -> storage.Bucket:
    return get_firebase_bucket()