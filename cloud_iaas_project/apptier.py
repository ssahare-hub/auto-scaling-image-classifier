from helper import *
import boto3

# recieve from request sqs and get job id (image name)
sqs = boto3.client('sqs')
# Create a SQS queue
create_queue('SQS_QUEUE_1',
             {'DelaySeconds': '0',
              'MessageRetentionPeriod': '86400'}
)
# Get URL for SQS queue
response = sqs.get_queue_url('SQS_QUEUE_1')
# fetch job image from S3 using job id (image name)

# process image using local model
# store result in s3  
# send message in response queue
# check queue for any pending requests, if yes repeat
# if queue empty, terminate