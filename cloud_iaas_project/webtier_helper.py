from werkzeug.utils import secure_filename
from helper import *
from constants import *
import time


# post / upload images and start aws functions
# aws functions using helper ->
def process_image(request_queue_url, path, object_name, job_id):
    # TODO: Add uniqueness to filename
    # store images to s3
    print('uploading file {} to {}'.format(object_name, BUCKET_NAME))
    upload_file(path, BUCKET_NAME, object_name)

    # queue image_name in request queue
    # TODO: Fill these and include job id somewhere!
    message_attr = {}
    message_body = object_name
    print('sending message {} to {} '.format(message_body, request_queue_url))
    send_message(request_queue_url, message_attr, job_id, message_body)


def spawn_processing_apps(request_queue_url, job_id):
    # wait for 1 second before starting
    # time.sleep(1)
    queue_length = get_one_queue_attribute(request_queue_url)
    queue_length = int(queue_length)
    print('queue length is {}'.format(queue_length))

    # TODO: retrieve number of live app tiers and subtract from max_app_tiers
    num_instances = min(queue_length, MAX_APP_TIERS)

    # spawn ec2 instances according to request queue length
    # response = create_instance(
    #     KEY_NAME,
    #     SECURITY_GROUP_ID,
    #     image_id=AMI_IMAGE_ID,
    #     min_count=num_instances,
    #     max_count=num_instances
    # )

    print('Simulating {} - running of {} instances'.format(job_id, num_instances))

    # print('response for creating instances was as follows ->\n{}'.format(response))


# start listening to response queue for results
def listen_for_results(socketio, response_queue_url, job_id, job_dictionary):
    # queue_length = get_one_queue_attribute(response_queue_url)
    results_received = 0
    job_length = job_dictionary[job_id]
    # TODO: IMPROVE THIS LOOP!!!!
    while results_received != job_length:
        # TODO: insert logic to receive messages!??
        result = receive_message(RESPONSE_QUEUE_NAME)
        # once received, increase counter...
        if result is not None:
            results_received += 1
            # TODO: retrieve from s3? or send it back to client
            # send results back to user using sockets
            socketio.emit(
                'partial_result', 'extract from result and format result-pair'
            )
    # TODO: when all results recieved, verify all apptier instances are stopped


def setup_aws_resources():
    #   create bucket if doesn't exist
    #   might add this inside upload_file / read_from_bucket ..
    create_bucket(BUCKET_NAME)

    #   create queue if doesn't exist
    request_queue_url = create_queue(REQUEST_QUEUE_NAME, QUEUE_ATTRIBUTES)

    #   create queue if doesn't exist
    response_queue_url = create_queue(RESPONSE_QUEUE_NAME, QUEUE_ATTRIBUTES)

    return request_queue_url, response_queue_url


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
