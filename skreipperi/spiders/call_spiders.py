from allSpiders import jobPosts
from flask import Flask, jsonify, Response
from json import JSONEncoder
import json


class JobEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

app = Flask(__name__) #3000
@app.route('/')
def index():
    jsonData = json.dumps(jobPosts, indent= 4, cls=JobEncoder)
    return Response(jsonData, mimetype='application/json')
app.run()
