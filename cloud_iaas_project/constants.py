# DO NOT CHANGE VALUES FOR THIS FILE
# EVEN OUTSIDE THIS FILE !!!!

REQUEST_QUEUE_NAME = 'requests_sss.fifo'
RESPONSE_QUEUE_NAME = 'response_sss.fifo'

MAX_RETRIES = 4

BUCKET_NAME = 'sss-cloud-bucket-9'

APP_TIER_PREFIX = 'cc_sss_app_tier'

KEY_NAME = 'newkey'

SECURITY_GROUP_ID = 'sg-0c7f568aaf89e6cd9'

# replace this with custom ami with app tier logic!!
AMI_IMAGE_ID = 'ami-09fec7c58e976045c'
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
    'ReceiveMessageWaitTimeSeconds': '20',
    'VisibilityTimeout': '30',
    'ContentBasedDeduplication': 'true'
}

USERDATA = '''#!/bin/bash
/usr/bin/python3 /home/ubuntu/cloud_project/cloud_iaas_project/apptier.py'''

INSTANCE_PROFILE = {
    'Arn':'arn:aws:iam::869079644211:instance-profile/newrole',
}