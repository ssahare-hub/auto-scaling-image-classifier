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

# Start of image_classification function

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
# GET COUNT OF VISIBLE & INVISIBLE MESSAGES

def queue_length():
    noof_visible_messages = get_one_queue_attribute(queue_url, attribute_name= VISIBLE_MESSAGES)
    noof_invisible_messages = get_one_queue_attribute(queue_url, attribute_name= INVISIBLE_MESSAGES)
    length = int(noof_visible_messages) + int(noof_invisible_messages)
    return (length)

queue_len = queue_length()

#GET REQUEST & RESPONSE QUEUE URLS
job_url = get_queue_url(REQUEST_QUEUE_NAME)
response_queue_url = get_queue_url(RESPONSE_QUEUE_NAME)


while queue_len > 0:
# 1) receive message from request queue
    imageid_from_request_queue_url = receive_message(job_url, 1)
    message = imageid_from_request_queue_url['Messages'][0]
    job_id = message['Body']

# 2) get image from s3
    read_from_bucket(BUCKET_NAME, job_id)

# 3) process image and return result
    image_classification_output = image_classification(job_id)
    response_queue_message = job_id +" == "+image_classification_output

# 4) store result in s3 and put in response queue
    file_to_store = job_id + ".txt"
    s3_writetofile = open(file_to_store, "w+")
    s3_writetofile.write(response_queue_message)
    s3_writetofile.close()
    upload_file(file_to_store, RESULTS_BUCKET, file_to_store)
    send_message(response_queue_url, 'All', response_queue_message)

# 5) delete message from request queue
    receipt_handle = message['ReceiptHandle']
    delete_message(response_queue_url, receipt_handle)
    print('Received and deleted message: %s' % message)
