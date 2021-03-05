import boto3

import boto3

# Create SQS client
sqs = boto3.client('sqs')


# Get URL for SQS queue
response = sqs.get_queue_url(QueueName='SQS_QUEUE_NAME')


# Delete SQS queue
#sqs.delete_queue(QueueUrl='SQS_QUEUE_NAME')

queue_url = response['QueueUrl']

# Send message to SQS queue
'''response1 = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=0,
    MessageBody=(
        'Information about current vizag Times fiction bestseller for '
    )
)'''

#print(response1['MessageId'])

response2 = sqs.receive_message(QueueUrl=queue_url)

print (response2)
print(len(response2))

message = response2['Messages'][0]
print (message)

receipt_handle = message['Body']

print(receipt_handle)

'''sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message)'''
