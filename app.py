import os
import datetime
from flask import Flask
from flask import g
from flask import jsonify
from flask import json
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import make_response
from werkzeug import secure_filename
import pymongo
from pymongo import Connection, GEO2D
from bson import BSON
from bson import json_util
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import uuid
import random

app = Flask(__name__)
BASE_URL = "http://guarded-earth-9510.herokuapp.com/"

def mongo_conn():
    # Format: MONGOHQ_URL: mongodb://<user>:<pass>@<base_url>:<port>/<url_path>
    if os.environ.get('MONGOHQ_URL'):
        return Connection(os.environ['MONGOHQ_URL'])
    else:
        #return Connection('mongodb://heroku:07d95f7ef938ef3b2fc664f8734c23c9@alex.mongohq.com:10046/app8563631')
        return Connection()


@app.route('/test', methods=['GET'])
def test_data():
    # Get your DB
    mongo_conn().app8563631.whispers.create_index([("loc", GEO2D)])
    return render_template("test.html")    

@app.route('/', methods=['GET'])
def hello():
    #mongo_conn().app8563631.whispers.remove()
    return render_template("index.html")

@app.route('/upload_geoaudio', methods=['POST'])
def upload_geoaudio():
    # Get your DB
    connection = mongo_conn()

    db = connection.app8563631

    #whisper = request.files['whisper']
    #filename = secure_filename(whisper.filename)
    whisper = request.json['whisper']

    # Save the whisper to S3
    conn = S3Connection('AKIAIVNDDEXUH2KCJWJA', 'KdY8E/dfj1UXPs1wHXwYxllUr+hrGGNoVvfaKuMV')
    bucket = conn.create_bucket('whisperly')
    k = Key(bucket)
    k.key = str(uuid.uuid4())
    k.set_metadata("Content-Type", 'audio/aac')
    k.set_contents_from_string(whisper)


    # Get the geolocation data
    whisperData = {
        "loc": [float(request.json['longitude']), float(request.json['latitude'])],
        "s3_key": k.key
    }

    # Get the collection
    whispers = db.whispers

    # Insert it into the db
    whispers.insert(whisperData)

    # Return all the whispers?
    json_docs = [json.dumps(doc, default=json_util.default) for doc in whispers.find()]
    return '\n'.join(json_docs)

@app.route('/near_points', methods=['POST'])
def near_points():
    latitude = float(request.json['latitude'])
    longitude = float(request.json['longitude'])
    connection = mongo_conn()
    db = connection.app8563631
    whispers = db.whispers
    near = whispers.find({"loc": {"$near": [latitude, longitude]}}).limit(50)
    results = [{'lat': doc['loc'][0], 'lng': doc['loc'][1], 'link': ('/sounds/' + doc['s3_key'])} for doc in near]
    return jsonify(items=results)

@app.route('/sounds/<filename>', methods=['GET'])
def play_sound(filename):
    filename = "http://cs.utexas.edu/~elie/" + str(random.randint(0,9) + ".m4a"
    return render_template('player.html', filename=filename)
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
