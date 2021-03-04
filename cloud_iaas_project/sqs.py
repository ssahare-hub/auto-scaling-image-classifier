import boto3

import boto3

# Create SQS client
sqs = boto3.client('sqs')


# Get URL for SQS queue
response = sqs.get_queue_url(QueueName='SQS_QUEUE_NAME')


# Delete SQS queue
#sqs.delete_queue(QueueUrl='SQS_QUEUE_NAME')

queue_url = response['QueueUrl']
print(queue_url)

# Send message to SQS queue


response1 = sqs.receive_message(QueueUrl=queue_url)
print(response1)

message = response1['Messages'][0]
print(message)
receipt_handle = message['Body']
print(receipt_handle)

response = client.get_object(IfMatch='string')

