import logging
import boto3
from botocore.exceptions import ClientError
import botocore

# functions for AWS ->
# SQS
# create queue (if it doesn't exist)
def create_queue(queue_name, attributes):
    # should return queue url!!!
    sqs = boto3.resource('sqs')
    SQS_QUEUE_NAME = queue_name
    # Create a SQS queue
    response = sqs.create_queue(QueueName=SQS_QUEUE_NAME,Attributes={'DelaySeconds': '0','MessageRetentionPeriod': '600','ReceiveMessageWaitTimeSeconds': '20'})
    print("Queue URL ->" , response.url)
    for response in sqs.queues.all():
        print("All Queues ->" ,response.url)

# create_queue('xyz','a')

def get_queue_attributes(queue_url, attribute_names):
    pass

# send message to queue
def send_message(queue_url, message_attributes, message_body):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        # DelaySeconds=10,
        MessageAttributes=message_attributes,
        # {
        # 'Title': {
        #     'DataType': 'String',
        #     'StringValue': 'The Whistler'}},
        MessageBody=message_body
        # ('hello')
    )
    
    print(response['MessageId'])
    
m=('hi')
ma={'Title': {'DataType': 'String','StringValue': 'The Whistler'}}
u="https://queue.amazonaws.com/869079644211/xyz"
# send_message(u,ma,m)


# recieve message from queue (wait time as a variable)
def receive_message(queue_name):
    # attribute_names, 
    # max_num_message, 
    # message_attribute_names, 
    # visibility_timeout, 
    # wait_time_seconds
    print("eneters rece")
    sqs=boto3.resource('sqs')
    # s=boto3.client('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    qurl= queue.url
    print("printing ur", qurl)
    for message in queue.receive_messages():
        print('{0}'.format(message.body))
        message.delete()
#     response=s.recieve_message( QueueUrl=qurl,AttributeNames=['SentTimestamp'], MaxNumberOfMessages=1,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
#     message = response['Messages'][0]
#     receipt_handle = message['ReceiptHandle']
#     sqs.delete_message(
#     QueueUrl=qurl,
#     ReceiptHandle=receipt_handle)
    print('Received and deleted message: %s' % message)


# receive_message('xyz')


# delete queue??
def delete_queue(queue_url):
    sqs=boto3.client('sqs')
    sqs.delete_queue(QueueUrl=queue_url)
    print('Deleted queue', queue_url)

# delete_queue('https://queue.amazonaws.com/869079644211/xyz')

# S3
# create bucket (if it doesn't exist)
def create_bucket(bucket_name, region=None):
    # return success status
    s3 = boto3.client('s3')
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
            print("bucket created", bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name,
                             CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# create_bucket('shreyapat1')
# add to bucket
def upload_file(file_name, bucket_name, object_name):
    # return success status
    s3 = boto3.client('s3')
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket_name, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

    # print('Existing buckets:')
    # for bucket in response['Buckets']:
    #     print(f'-------{bucket["Name"]}------')
    #     for obj in s3.Bucket(bucket_name).objects.all():
    #         print(obj)

# git upload_file('/Users/shreyapatel/cloud_project/cloud_iaas_project/pictures/cake.jpg','shreyapat1', 'cake1')
# read from bucket
def read_from_bucket(bucket_name, object_name,expiration=7200):
    # return file from bucket
    # checkk if bucket exists
    # s3 = boto3.resource('s3')
    # s3_connection = boto.connect_s3()
    # bucket = s3_connection.get_bucket(bucket_name, validate=False)
    # exists = s3_connection.lookup(bucket_name)
    # obj=s3.Object(bucket_name,itemname)
    # b=s3.Bucket(bucket_name)
    # obj = s3.Object(bucket_name, object_name)
    # body = obj.get()['Body'].read()
    # # for obj in b.objects.all():
    # #     key=obj.key
    # #     body=obj.get()['Body'].read()
    # print(obj)
    # print(body)
    # with open('myfile.png', 'w') as f:
    #     f.write(body)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    print(response)
    

# read_from_bucket('shreyapat1','cake')
# delete from bucket
def delete_from_bucket(bucket_name, object_name):
    # s3 = boto3.client('s3')
    pass

# delete bucket??
def delete_bucket(bucket_name):
    pass

# EC2
# create instances (ami code)
def create_instance(
    key_name, 
    sec_group_ids,
    image_id = 'ami-0ee8cf7b8a34448a6', 
    instance_type = 't2.micro', 
    min_count = 1, 
    max_count = 1
):
    pass

# start/stop instances ??
def interact_with_instance(instance_id, action):
    # action can be 'start' or 'stop'
    pass

# terminate instance? (self)
def terminate_instance(instance_id):
    pass