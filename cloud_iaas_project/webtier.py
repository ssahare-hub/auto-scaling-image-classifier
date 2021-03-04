import time
import os
from flask import Flask, render_template, flash, request, redirect, url_for, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from threading import Thread, Timer

# Below import might change in production
import constants
print(constants.REQUEST_QUEUE_NAME)

# constants for uploads and allowed extensions
is_get = True
images = []
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# host flask server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# create socket connection
socketio = SocketIO(app)
# allow requests from cross origin domains
socketio.init_app(app, cors_allowed_origins="*")

# GET & POST endpoint at '/'


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        # send upload start event
        socketio.emit('upload_start', len(images))
        # start processing uploaded images
        recieved = request.files.getlist("file")
        for file in recieved:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                images.append(file)
                print('file uploaded -> ', filename)
                # push_to_SQS(images)

        # uploading finished, send processing images event
        socketio.emit('processing_start', 'done')
        print('files', images)
        is_get = False
    else:
        is_get = True
    # get / render front end page
    return render_template('index.html', is_get=is_get, num_images=len(images))

# socket io listeners and event emitters start here


@socketio.on('connect')
def connected():
    print('connected')
    socketio.emit('on_connect', is_get)


@socketio.on('disconnect')
def disconnected():
    print('disconnected')


# post / upload images and start aws functions

# aws functions using helper ->
#   store images to s3
#   create queue if doesn't exist
#       queue image_name in request queue
#   spawn ec2 instances according to request queue length
#   start listening to response queue for results
#       send results back to user using sockets
#       when all results recieved, verify all apptier instances are stopped
#   END

if __name__ == '__main__':
    print('starting listening to server events')
    socketio.run(
        app        # , host='0.0.0.0'
        , port=5000
    )
