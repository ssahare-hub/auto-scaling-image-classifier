from helper import *
import boto3
import os
sqs = boto3.client('sqs')

while(True):
# recieve from request sqs and get job id (image name)
    response = sqs.recieve_message(QueueUrl='string')
    message = response1['Messages'][0]
    job_id = message['Body']

# fetch job image from S3 using job id (image name)
    s3 = boto3.resource('s3' )
    image_tobe_processed = read_from_bucket('cc-asu-project', job_id)

# process image using local model
    os.system("aws s3 cp s3://cc-asu-project/" + str(image_tobe_processed) + " 1")
    delete_from_bucket(bucket_name, object_name)
    out = open("{fname}.txt".format(fname = image_tobe_processed), "w")
    os.system("python3 image_classification.py 1 > {fname}.txt".format(fname = image_tobe_processed))
    os.system("rm -rf 1")

# store result in s3
    os.system("aws s3 cp {fname}.txt s3://cc-project-results/{fname}.txt".format(fname = image_tobe_processed))
# send message in response queue
# check queue for any pending requests, if yes repeat
# if queue empty, terminate