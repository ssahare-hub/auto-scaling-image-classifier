# host flask server at /
# create socket connection on page load

# get / render front end page
# post / upload images and start aws functions

# aws functions using helper ->
#   store images to s3
#   create queue if doesn't exist
#       queue image_name in request queue 
#   spawn ec2 instances according to request queue length
#   start listening to response queue for results
#       send results back to user using sockets
#       when all results recieved, verify all apptier instances are stopped
#   END



