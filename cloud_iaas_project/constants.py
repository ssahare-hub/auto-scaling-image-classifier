# DO NOT CHANGE VALUES FOR THIS FILE
# EVEN OUTSIDE THIS FILE !!!!

REQUEST_QUEUE_NAME = 'requests_sai.fifo'
RESPONSE_QUEUE_NAME = 'response_sai.fifo'

MAX_RETRIES = 4

BUCKET_NAME = 'sai-cloud-bucket'

APP_TIER_PREFIX = 'sss_app_tier_'

KEY_NAME = 'Cloud Computing - ASU - Project1'
SECURITY_GROUP_ID = 'sg-03c646f82a7068326'

# replace this with custom ami with app tier logic!!
AMI_IMAGE_ID = 'ami-016f125ec17a8c8dd'
OG_AMI_IMAGE_ID = 'ami-0ee8cf7b8a34448a6'

MIN_APP_TIERS = 0
MAX_APP_TIERS = 19

UPLOAD_FOLDER = './uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = 'SECRET!!!'

VISIBLE_MESSAGES = 'ApproximateNumberOfMessages'
INVISIBLE_MESSAGES = 'ApproximateNumberOfMessagesNotVisible'

QUEUE_ATTRIBUTES = {
    'FifoQueue': 'true',
    'ReceiveMessageWaitTimeSeconds': '5',
    'VisibilityTimeout': '30',
    'ContentBasedDeduplication': 'true'
}

USERDATA = '''#!/bin/bash
/usr/bin/python3 /home/ubuntu/cloud_project/cloud_iaas_project/apptier.py'''

INSTANCE_PROFILE = {
    'Arn':'arn:aws:iam::871530961586:instance-profile/sample-webtier'
}