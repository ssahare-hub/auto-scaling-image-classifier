import boto3
from werkzeug.utils import secure_filename
from helper import *
from constants import *
import json
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
    body_object = {
        'task_id': object_name,
        'job_id': job_id
    }
    body = json.dumps(body_object)
    print('sending message {} to {} '.format(body, request_queue_url))
    send_message(request_queue_url, message_attr, job_id, body)


def spawn_processing_apps(request_queue_url, job_id):
    queue_length = get_one_queue_attribute(request_queue_url)
    queue_length = int(queue_length)
    print('queue length is {}'.format(queue_length))

    # TODO: retrieve number of live app tiers and subtract from max_app_tiers
    num_running = get_running_app_tiers_ids()
    max_new = MAX_APP_TIERS - num_running

    num_instances = min(queue_length, max_new)

    # spawn ec2 instances according to request queue length
    create_instance(
        KEY_NAME,
        SECURITY_GROUP_ID,
        APP_TIER_PREFIX,
        image_id=AMI_IMAGE_ID,
        min_count=num_instances,
        max_count=num_instances
    )

    print('For jobid {} - will create {} instances'.format(job_id, num_instances))


def get_running_app_tiers_ids():
    current_instance_id = get_instance_id()
    ec2_client = boto3.client('ec2')
    reservations = ec2_client.describe_instances()['Reservations']
    instance_ids = [r['Instances'][0]['InstanceId'] for r in reservations]
    if current_instance_id in instance_ids:
        instance_ids.remove(current_instance_id)
    return len(instance_ids)

# start listening to response queue for results


def listen_for_results(socketio, response_queue_url, job_id, job_dictionary):
    # queue_length = get_one_queue_attribute(response_queue_url)
    results_received = 0
    job_length = job_dictionary[job_id]
    socketio.emit('processing_start', job_length)
    print('Starting to listen for {} results '.format(job_length))
    # TODO: IMPROVE THIS LOOP!!!!
    while results_received != job_length:
        print('Trying to receive message at {}'.format(time.time()))
        # TODO: insert logic to receive messages!??
        resp = receive_message(response_queue_url, 1)
        # once received, increase counter...
        if 'Messages' in resp:
            message = resp['Messages'][0]
            result = message['Body']
            print('result found as {} , processing'.format(result))
            results_received += 1
            # send results back to user using sockets
            socketio.emit(
                'partial_result', result
            )
            print('processing complete so deleting message')
            receipt_handle = message['ReceiptHandle']
            delete_message(response_queue_url, receipt_handle)
        print('-'*30)
    print('processing has ended for job with {} results'.format(job_length))
    print('-'*50)
    socketio.emit('processing_end', '')
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
