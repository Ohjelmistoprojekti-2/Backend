from allSpiders import jobPosts
from flask import Flask, jsonify, Response
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
    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    return Response(jsonData, mimetype='application/json')
if __name__ == '__main__':
    app.run()
