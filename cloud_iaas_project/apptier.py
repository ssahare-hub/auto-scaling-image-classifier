import numpy as np
import json
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import torch
from helper import *
import time
print('importing finished')
# Start of image_classification function


def image_classification(job_id):
    img = Image.open(r"{x}".format(x=job_id))
    model = models.resnet18(pretrained=True)
    model.eval()
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)
    with open('/home/ubuntu/cloud_project/cloud_iaas_project/imagenet-labels.json') as f:
        labels = json.load(f)
    result = labels[np.array(predicted)[0]]
    return(result)

# end of function


# GET REQUEST & RESPONSE QUEUE URLS
request_queue_url = get_queue_url(REQUEST_QUEUE_NAME)
response_queue_url = get_queue_url(RESPONSE_QUEUE_NAME)

jobs_processed = 0

CURR_RETRIES = 0
while (CURR_RETRIES < MAX_RETRIES):
    # 1) receive message from request queue
    imageid_from_request_queue_url = receive_message(request_queue_url, 1)
    if 'Messages' in imageid_from_request_queue_url:
        message = imageid_from_request_queue_url['Messages'][0]
        body_string = message['Body']
        print('message was -> {}'.format(body_string))
        body = json.loads(body_string)
        image_id = body['task_id']
        job_id = body['job_id']
        print('reading from bucket {}'.format(BUCKET_NAME))
# 2) get image from s3
        read_from_bucket(BUCKET_NAME, '{}{}'.format(S3_INPUT_FOLDER, image_id), image_id)

# 3) process image and return result
        image_classification_output = image_classification(image_id)
        response_queue_message = '({}, {})'.format(
            image_id, image_classification_output)
        print('result classification was {}'.format(response_queue_message))

# 4) store result in s3 and put in response queue
        file_to_store = '{}_Result.txt'.format(image_id)
        s3_writetofile = open(file_to_store, "w+")
        s3_writetofile.write(response_queue_message)
        s3_writetofile.close()

        upload_file(file_to_store, BUCKET_NAME, '{}{}'.format(S3_OUTPUT_FOLDER, file_to_store))
        print('uploaded file to bucket')
        send_message(response_queue_url, {}, job_id, response_queue_message)
        print('sent message to queue')

# 5) delete message from request queue
        receipt_handle = message['ReceiptHandle']
        delete_message(request_queue_url, receipt_handle)
        print('deleted message from queue')

# 6) Listen for requests before terminating
        CURR_RETRIES = 0
        jobs_processed += 1
    else:
        CURR_RETRIES += 1

# 7) Add logic to terminate instance
instanceid_to_kill = get_instance_id()
print('instance id - {}, processed {} jobs and will be terminated now'.format(
    instanceid_to_kill, jobs_processed))
terminate_instance(instanceid_to_kill)
