from firebase_admin.firestore import client
from firebase_admin import initialize_app, credentials
from google.cloud import datastore
from google.cloud.firestore_v1beta1 import GeoPoint
from google.cloud.exceptions import Conflict
# Dependencies : google-cloud google-cloud-firestore firebase_admin


def init():
    cred = credentials.Certificate("firebase_credentials.json")
    initialize_app(cred)


def get_col(name):
    return cli.collection(name)


def get_docs_in_col(col):
    # Returns a generator
    return col.get()


def get_doc(name):
    return cli.collection(name)

# d = list(col.get())[0]
# d.to_dict()


def add_record(col, id, rec):
    print rec
    # col.document(id).set(rec)       ----- This will override existing document if id exists
    try:
        col.add(document_data=rec, document_id=id)
    except Conflict as f:
        if f.code == 409:
            raise Exception("Key '" + id + "'already exists\n===============")


CITY_COLLECTION = 'Cities'
try:
    cli = client()
except:
    init()
    cli = client()
