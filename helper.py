# functions for AWS ->

# SQS
# create queue (if it doesn't exist)
def create_queue(queue_name, attributes):
    # should return queue url!!!
    pass

# send message to queue
def send_message(queue_url, message_attributes, message_body):
    pass

# recieve message from queue (wait time as a variable)
def recieve_message(
    queue_name, 
    attribute_names, 
    max_num_message, 
    message_attribute_names, 
    visibility_timeout, 
    wait_time_seconds
):
    pass

# delete queue??
def delete_queue(queue_url):
    pass

# S3
# create bucket (if it doesn't exist)
def create_bucket(bucket_name):
    # return success status
    pass

# add to bucket
def upload_file(file_name, bucket_name, object_name):
    # return success status
    pass

# read from bucket
def read_from_bucket(bucket_name, object_name):
    # return file from bucket
    pass

# delete from bucket
def delete_from_bucket(bucket_name, object_name):
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