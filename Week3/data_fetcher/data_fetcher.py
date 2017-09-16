import os
import sys
import time
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient
import mongodb_client
import zillow_web_scraper_client


# RabbitMQ config
CLOUD_AMQP_URL = '''amqp://ihxuqoiv:2x0xLmYxyg-06B_XgRQfjE-DZ3LK3IyI@zebra.rmq.cloudamqp.com/ihxuqoiv'''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'

# mongodb config
PROPERTY_TABLE_NAME = 'property'

# Similar property scraper switch
FETCH_SIMILAR_PROPERTIES = False

SECONDS_IN_ONE_DAY = 3600 * 24
SECONDS_IN_ONE_WEEK = SECONDS_IN_ONE_DAY * 7
WAITING_TIME = 3


cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

def handle_message(msg):
	task = json.loads(msg)
	
	if(not isinstance(task, dict) or
	   not 'zpid' in task or
	   task['zpid'] is None):
		return

	zpid = task['zpid']
	

	# Scrape the zillow for  details
	property_detail = zillow_web_scraper_client.get_property_by_zpid(zpid)
	property_detail['last_update'] = time.time()
		
	# Update doc in db
	db = mongodb_client.getDB()
	db[PROPERTY_TABLE_NAME].replace_one({'zpid': zpid}, property_detail, upsert=True)

	if FETCH_SIMILAR_PROPERTIES:
		# get its similar properties
		similar_zpid = zillow_web_scraper_client.get_similar_homes_for_sale_by_id(zpid)

		# generate tasks for similar zpid
		for zpid in similar_zpid:
			old = db[PROPERTY_TABLE_NAME].find_one({'zpid': zpid})
			if (old is not None and
			    time.time() - old['last_update'] < SECONDS_IN_ONE_WEEK):
				continue
			cloudAMQP_client.sendDataFetcherTask({'zpid': zpid})	
	
# Main thread
while True:
	#fetch a message
	if cloudAMQP_client is not None:
		msg = cloudAMQP_client.getDataFetcherTask()
		if msg is not None:
			handle_message(msg)
		time.sleep(WAITING_TIME)
