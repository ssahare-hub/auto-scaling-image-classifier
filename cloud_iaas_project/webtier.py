import uuid
import time
import os
from flask import Flask, render_template, flash, request, redirect, url_for, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from threading import Thread, Timer

# Below import might change in production
import constants
from helper import *

# constants for uploads and allowed extensions
is_get = True
request_queue_url = ''
response_queue_url = ''
images = []
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
job_dictionary = {}


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
    is_get = (request.method == 'GET')
    job_id = str(uuid.uuid4())
    recieved = []
    if not is_get:
        # start processing uploaded images
        recieved = request.files.getlist("file")
        for file in recieved:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                images.append(file)
                print('file uploaded -> ', filename)
            process_image(file, job_id)

        job_dictionary[job_id] = len(images)
        print('files', images)

        # start in another thread ->
        # spawn_processing_apps(job_id)
        # listen_for_results(job_id)

    # get / render front end page
    return render_template(
        'index.html',
        is_get=is_get,
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


# post / upload images and start aws functions
# aws functions using helper ->
def process_image(image, job_id):
    # TODO: Add uniqueness to filename
    image_name = secure_filename(image.filename)

    # store images to s3
    print('uploading image named {}'.format(image_name))
    # upload_file(image, constants.BUCKET_NAME, image_name)

    # queue image_name in request queue
    # TODO: Fill these and include job id somewhere!
    message_attr = {}
    message_body = {
        'image_name': image_name,
        'job_id': job_id
    }
    print('sending message {} to {} '.format(request_queue_url, message_body))
    # send_message(request_queue_url, message_attr, message_body)


def spawn_processing_apps(job_id):
    # add a new helper function -> get_queue_attributes
    attribute_names = 'ALL'
    attributes = get_queue_attributes(request_queue_url, attribute_names)

    # TODO: VERIFY THIS
    queue_length = attributes['Attributes']['ApproximateNumberOfMessages']

    # TODO: retrieve number of live app tiers and subtract from max_app_tiers
    num_instances = min(queue_length, constants.MAX_APP_TIERS)

    # spawn ec2 instances according to request queue length
    create_instance(
        constants.KEY_NAME,
        constants.SECURITY_GROUP_ID,
        image_id=constants.AMI_IMAGE_ID,
        min_count=num_instances,
        max_count=num_instances
    )

# start listening to response queue for results


def listen_for_results(job_id):
    attribute_names = 'ALL'
    attributes = get_queue_attributes(response_queue_url, attribute_names)
    # TODO: VERIFY THIS
    queue_length = attributes['Attributes']['ApproximateNumberOfMessages']
    results_received = 0
    job_length = job_dictionary[job_id]
    # TODO: IMPROVE THIS LOOP!!!!
    while results_received != job_length:
        # TODO: insert logic to receive messages!??
        result = recieve_message(
            constants.RESPONSE_QUEUE_NAME, None, None, None, None, None
        )
        # once received, increase counter...
        if result is not None:
            results_received += 1
            # TODO: retrieve from s3? or send it back to client
            # send results back to user using sockets
            socketio.emit(
                'partial_result', 'extract from result and format result-pair'
            )
    # when all results recieved, verify all apptier instances are stopped


def setup_aws_resources():
    #   create bucket if doesn't exist
    #   might add this inside upload_file / read_from_bucket ..
    create_bucket(constants.BUCKET_NAME)

    #   TODO: Add attributes
    attributes = {

    }

    #   create queue if doesn't exist
    request_queue = create_queue(constants.REQUEST_QUEUE_NAME, attributes)
    request_queue_url = request_queue['QUEUE_URL']

    #   create queue if doesn't exist
    response_queue = create_queue(constants.RESPONSE_QUEUE_NAME, attributes)
    response_queue_url = response_queue['QUEUE_URL']

    return request_queue_url, response_queue_url


# main block starts here
# request_queue_url, response_queue_url = setup_aws_resources()

if __name__ == '__main__':
    print('starting listening to server events')
    socketio.run(
        app        # , host='0.0.0.0'
        , port=5000
    )
