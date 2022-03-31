from flask import Flask, request, Response
from json import JSONEncoder
import json
from flask_cors import CORS
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


cred = credentials.Certificate('firebaseSDK.json')

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