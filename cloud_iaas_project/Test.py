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

response = sqs.get_queue_url(QueueName='SQS_QUEUE_NAME')

job_url = response['QueueUrl']

response1 = sqs.send_message(
    QueueUrl= job_url,
    MessageBody=('test_22.JPEG'))

# recieve from request sqs and get job id (image name)
response2 = sqs.receive_message(
    QueueUrl= job_url,
    AttributeNames=['All'],
    MessageAttributeNames=['All'],
    MaxNumberOfMessages=1,
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)
message = response2['Messages'][0]
job_id = message['Body']
print(job_id)

# fetch job image from S3 using job id (image name)
os.system("aws s3 cp s3://cc-asu-project/{x} {x}".format(x=job_id))
os.system("aws s3 cp s3://cc-project-results/imagenet-labels.json imagenet-labels.json")

# process image using local model
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
output = image_classification(job_id)
print(job_id +" == "+output)
'''delete_from_bucket(bucket_name, object_name)
    out = open("{fname}.txt".format(fname = image_tobe_processed), "w")

# store result in s3
    os.system("aws s3 cp {fname}.txt s3://cc-project-results/{fname}.txt".format(fname = image_tobe_processed))
# send message in response queue
# check queue for any pending requests, if yes repeat'''