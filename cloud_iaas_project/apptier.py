from helper import *
import boto3
sqs = boto3.client('sqs')
# recieve from request sqs and get job id (image name)
response = sqs.receive_message(QueueUrl='string')
message = response1['Messages'][0]
job_id = message['Body']
# fetch job image from S3 using job id (image name)

# process image using local model
# store result in s3  
# send message in response queue
# check queue for any pending requests, if yes repeat
# if queue empty, terminate