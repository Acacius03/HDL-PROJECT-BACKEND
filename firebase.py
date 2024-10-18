# # import json
# import firebase_admin
# from firebase_admin import credentials, firestore, storage

# cred = credentials.Certificate('firebase_config.json')
# firebase_admin.initialize_app(cred)

# firestore_db = firestore.client()
# storage_db = storage.bucket('gs://hdl-project-36053.appspot.com/Fingerprints')
# print(storage_db)

# # test firestore
# # data = {
# #     'name': 'Henry Sy',
# #     'LoggedIn': True
# # }

# # doc_ref = firestore_db.collection('students').document()
# # doc_ref.set(data)
# # print('Document ID:', doc_ref.id)

# # firestore_client = firestore_async.client(firebase) #asynchronous

