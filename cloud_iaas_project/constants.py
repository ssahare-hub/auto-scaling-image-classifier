# DO NOT CHANGE VALUES FOR THIS FILE
# EVEN OUTSIDE THIS FILE !!!!

REQUEST_QUEUE_NAME = 'requests_sss.fifo'
RESPONSE_QUEUE_NAME = 'response_sss.fifo'

MAX_RETRIES = 4

BUCKET_NAME = 'sss-cloud-bucket'

APP_TIER_PREFIX = 'sss_app_tier_'

KEY_NAME = 'aws-kp-1'

SECURITY_GROUP_ID = 'sg-0c3a65f539fa2240a'

# replace this with custom ami with app tier logic!!
AMI_IMAGE_ID = 'ami-0478128c959c87087'
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
    'Arn':'arn:aws:iam::115873875546:instance-profile/EC2_FA_Role',
}