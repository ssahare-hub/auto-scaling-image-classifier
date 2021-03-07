from .helper import *
import boto3
import os
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import json
import sys
import numpy as np
sqs = boto3.client('sqs')
s3 = boto3.resource('s3')

# Start of a new function

def image_classification(job_id):
    img = Image.open(r"{x}".format(x=job_id))
    model = models.resnet18(pretrained=True)
    model.eval()
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)

    with open('./imagenet-labels.json') as f:
        labels = json.load(f)
    result = labels[np.array(predicted)[0]]
    return(result)

# end of function

while len(queue) > 0:

# 1) Getting queue url
    request_queue_url = get_queue_attributes(queue_url= REQUEST_QUEUE_NAME, attribute_names= 'url')
    job_url = request_queue_url['QueueUrl']

# 2) receive message from request queue
    imageid_from_request_queue_url = sqs.receive_message(
        QueueUrl= job_url,
        AttributeNames=['All'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1,
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = imageid_from_request_queue_url['Messages'][0]
    job_id = message['Body']

# 3) get image from s3
    read_from_bucket(BUCKET_NAME, job_id, expiration=7200)

# 4) process image and return result

    image_classification_output = image_classification(job_id)
    response_queue_message = job_id +" == "+image_classification_output

# 5) store result in s3 and put in response queue
#TODO write results into a text file a store in the s3
    file_to_store = job_id + ".txt"
    s3_writetofile = open(file_to_store, 'w')
    s3_writetofile.write(response_queue_message)
    s3_writetofile.close()

    upload_file(file_to_store, RESULTS_BUCKET, file_to_store)
    sendmessage_to_responsequeue = sqs.get_queue_url(
                    QueueName= RESPONSE_QUEUE_NAME
    )

    response_url = sendmessage_to_responsequeue['QueueUrl']
    send_message(response_url, message_attributes, response_queue_message)

# 6) delete message from request queue
    sqs.delete_message(
        QueueUrl=job_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
# check queue for any pending requests, if yes repeat'''
