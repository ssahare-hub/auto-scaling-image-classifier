from helper import *

# recieve from request sqs and get job id (image name)
create_queue(image,)
# fetch job image from S3 using job id (image name)
# process image using local model
# store result in s3  
# send message in response queue
# check queue for any pending requests, if yes repeat
# if queue empty, terminate