from flask import Flask, request, Response
from json import JSONEncoder
import os
from flask_cors import CORS
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

private_key_id = os.getenv('private_key_id')
private_key = os.getenv('private_key')
client_email = os.getenv('client_email')
client_id = os.getenv('client_id')

testidict = {
    "type": "service_account",
    "project_id": "ohjelmistoprojekti2",
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9h6ca%40ohjelmistoprojekti2.iam.gserviceaccount.com"
}

cred = credentials.Certificate(testidict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ohjelmistoprojekti2-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference("/")


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

app = Flask(__name__) #3000
CORS(app)
@app.route('/api/tyopaikat')
def index():

    #print(request.headers.get('API-KEY'))

    #if request.headers.get('API-KEY'):
   #     api_key = request.headers.get('API-KEY')
   # else:
      #  return {"message": "Please provide an API key"}, 400
    #if request.method == "GET" and api_key == "API KEY ON JUHOLLA .ENV TIEDOSTOSSA":
        data = ref.get()
        return Response(data, mimetype='application/json')
    #else:
        #return {"message": "The provided API key is not valid"}, 403

    
if __name__ == '__main__':
    app.run()