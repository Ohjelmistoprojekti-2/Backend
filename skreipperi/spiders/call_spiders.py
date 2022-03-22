from allSpiders import jobPosts
from flask import Flask, request, Response
from json import JSONEncoder
import json
from flask_cors import CORS


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

app = Flask(__name__) #3000
CORS(app)
@app.route('/api/tyopaikat')
def index():

    if request.json:
            api_key = request.json.get("API-KEY")
    else:
        return {"message": "Please provide an API key"}, 400
    if request.method == "GET" and api_key == "6cc1d83f-0e10-4906-a5e1-1f6016f093bc":
        jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
        return Response(jsonData, mimetype='application/json')
    else:
        return {"message": "The provided API key is not valid"}, 403

    
if __name__ == '__main__':
    app.run()


