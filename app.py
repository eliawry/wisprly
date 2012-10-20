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
from pymongo import Connection
from bson import BSON
from bson import json_util
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

app = Flask(__name__)

def mongo_conn():
    # Format: MONGOHQ_URL: mongodb://<user>:<pass>@<base_url>:<port>/<url_path>
    if os.environ.get('MONGOHQ_URL'):
        return Connection(os.environ['MONGOLAB_URI'])
    else:
        return Connection()
    

@app.route('/', methods=['GET', 'POST'])
def hello():
    # Get your DB
    connection = mongo_conn()

    db = connection.my_database
    
    if request.method == 'POST':
        whisper = request.files['whisper']
        filename = secure_filename(whisper.filename)
        conn = S3Connection('AKIAJHIOLSDVACJCJXWQ', '2BS/TR7pCxMrR2stu2BSGVjvne0Dz8EBEfHjwEVX')
        bucket = conn.create_bucket('whisperly')
        k = Key(bucket)
        k.key = whisper.filename
        k.set_contents_from_string(whisper.read())

        whisper.seek(0)
        car = {"brand": whisper.readline().strip(),
               "model": whisper.readline().strip(),
               "date": datetime.datetime.utcnow()}

        # Get your collection
        cars = db.cars
        # Insert it
        cars.insert(car)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cars.find()]

        #json_docs = []
        for doc in cars.find():
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)
        return '\n'.join(json_docs)


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type="file" name="whisper">
         <input type="submit" value="Upload"></p>
    </form>
    '''


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
