from werkzeug.utils import secure_filename
from helper import *
from constants import *


# post / upload images and start aws functions
# aws functions using helper ->
def process_image(request_queue_url, image, job_id):
    # TODO: Add uniqueness to filename
    image_name = secure_filename(image.filename)

    # store images to s3
    print('uploading image named {}'.format(image_name))
    # upload_file(image, BUCKET_NAME, image_name)

    # queue image_name in request queue
    # TODO: Fill these and include job id somewhere!
    message_attr = {}
    message_body = {
        'image_name': image_name,
        'job_id': job_id
    }
    print('sending message {} to {} '.format(message_body, request_queue_url))
    # send_message(request_queue_url, message_attr, message_body)

def spawn_processing_apps(request_queue_url, job_id):
    # add a new helper function -> get_queue_attributes
    attribute_names = 'ALL'
    attributes = get_queue_attributes(request_queue_url, attribute_names)

    # TODO: VERIFY THIS
    queue_length = attributes['Attributes']['ApproximateNumberOfMessages']

    # TODO: retrieve number of live app tiers and subtract from max_app_tiers
    num_instances = min(queue_length, MAX_APP_TIERS)

    # spawn ec2 instances according to request queue length
    create_instance(
        KEY_NAME,
        SECURITY_GROUP_ID,
        image_id=AMI_IMAGE_ID,
        min_count=num_instances,
        max_count=num_instances
    )


# start listening to response queue for results
def listen_for_results(socketio, response_queue_url, job_id, job_dictionary):
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
            RESPONSE_QUEUE_NAME, None, None, None, None, None
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
    create_bucket(BUCKET_NAME)

    #   TODO: Add attributes
    attributes = {

    }

    #   create queue if doesn't exist
    request_queue = create_queue(REQUEST_QUEUE_NAME, attributes)
    request_queue_url = request_queue['QUEUE_URL']

    #   create queue if doesn't exist
    response_queue = create_queue(RESPONSE_QUEUE_NAME, attributes)
    response_queue_url = response_queue['QUEUE_URL']

    return request_queue_url, response_queue_url


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
