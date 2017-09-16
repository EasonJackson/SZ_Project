from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://ihxuqoiv:2x0xLmYxyg-06B_XgRQfjE-DZ3LK3IyI@zebra.rmq.cloudamqp.com/ihxuqoiv'

QUEUE_NAME = 'test_queue'

# initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# Send a message
#client.sendDataFetcherTask({'zpid':'test message'})

# Receive a message
client.getDataFetcherTask()
