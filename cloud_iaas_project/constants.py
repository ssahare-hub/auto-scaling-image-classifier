# DO NOT CHANGE VALUES FOR THIS FILE
# EVEN OUTSIDE THIS FILE !!!!

REQUEST_QUEUE_NAME = 'requests_sss.fifo'
RESPONSE_QUEUE_NAME = 'response_sss.fifo'

BUCKET_NAME = 'sss_cloud_bucket'

APP_TIER_PREFIX = 'sss_app_tier_'

KEY_NAME = 'aws-kp-1'

SECURITY_GROUP_ID = 'sg-0c3a65f539fa2240a'

# replace this with custom ami with app tier logic!!
AMI_IMAGE_ID = 'ami-0ee8cf7b8a34448a6'

MIN_APP_TIERS = 0
MAX_APP_TIERS = 19

UPLOAD_FOLDER = './uploads/'
DOWNLOAD_FOLDER = './downloads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = 'SECRET!!!'

VISIBLE_MESSAGES = 'ApproximateNumberOfMessages'
INVISIBLE_MESSAGES = 'ApproximateNumberOfMessagesNotVisible'

QUEUE_ATTRIBUTES = {
    'FifoQueue': 'true',
    'ReceiveMessageWaitTimeSeconds': '20',
    'VisibilityTimeout': '60',
    'ContentBasedDeduplication': 'true'
}
