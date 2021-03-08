import uuid
import time
import os
from flask import Flask, render_template, flash, request, redirect, url_for, request
from flask_socketio import SocketIO
from threading import Thread, Timer
from werkzeug.utils import secure_filename
from threading import Thread
from webtier_helper import * 
from constants import *
from helper import *

# constants for uploads and allowed extensions
is_get = True
request_queue_url = ''
response_queue_url = ''
images = []
job_dictionary = {}

# host flask server
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create socket connection
socketio = SocketIO(app)
# allow requests from cross origin domains
socketio.init_app(app, cors_allowed_origins="*")

# GET & POST endpoint at '/'
@app.route('/', methods=['GET', 'POST'])
def home_page():
    is_get = (request.method == 'GET')
    job_id = str(uuid.uuid4())
    recieved = []
    if not is_get:
        # start processing uploaded images
        recieved = request.files.getlist("file")
        for file in recieved:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                images.append(file)
                print('file uploaded -> ', filename)
            process_image(request_queue_url, path, filename, job_id)

        job_dictionary[job_id] = len(images)
        print('files', images)

        # start in another thread ->

        # spawn_processing_apps(req_q_url, job_id)
        spawner = Thread(target=spawn_processing_apps, args=(request_queue_url,job_id,))
        spawner.start()
        
        # listen_for_results(job_id)
        # listener = Thread(target=listen_for_results, args=(socketio, response_queue_url, job_id, job_dictionary,))
        # listener.start()

    # get / render front end page
    return render_template(
        'index.html',
        is_get=is_get,
        job_id=job_id,
        num_recieved=len(recieved),
        num_images=len(images)
    )

# socket io listeners and event emitters start here
@socketio.on('connect')
def connected():
    print('connected')
    socketio.emit('on_connect', is_get)


@socketio.on('disconnect')
def disconnected():
    print('disconnected')


# main block starts here
request_queue_url, response_queue_url = setup_aws_resources()

if __name__ == '__main__':
    print('starting listening to server events')
    socketio.run(
        app         
        , host='0.0.0.0'
        , port=5000
    )
