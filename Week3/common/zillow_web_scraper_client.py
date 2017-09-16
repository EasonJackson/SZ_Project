import random
import requests
import re
from lxml import html
from decimal import Decimal
from re import sub
from urllib import pathname2url
import socks
import socket

URL = ''' http://www.zillow.com'''
SEARCH_FOR_SALE_PATH = '''homes/for_sale'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''
GET_SIMILAR_HOMES_FOR_SALE_PATH = '''homedetails'''
IMAGE_URL_REGEX_PATTERN = '"z_listing_image_url":"([^"]+)",'
SIMILAR_HOMES_ZPID_REGEX_PATTERN = '\/(\d+)_zpid'

SEARCH_XPATH_FOR_ZPID = '''//div[@id='list-results']/div[@id='search-results']/ul[@class='photo-cards']/li/articles/@id'''
GET_INFO_XPATH_FOR_STREET_ADDR = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/text()'''
GET_INFO_XPATH_FOR_CITY_STATE_ZIP = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/span/text()'''
GET_INFO_XPATH_FOR_TYPE = '''//div[@class='loan-calculator-container']/div/@data-type'''
GET_INFO_XPATH_FOR_BEDROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][1]/text()'''
GET_INFO_XPATH_FOR_BATHROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][2]/text()'''
GET_INFO_XPATH_FOR_SIZE = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][3]/text()'''
GET_INFO_XPATH_FOR_SALE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div/text()'''
GET_INFO_XPATH_LIST_FOR_PRICE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div[@class='main-row  home-summary-row']/span/text()'''
GET_INFO_XPATH_FOR_LATITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='latitude']/@content'''
GET_INFO_XPATH_FOR_LONGITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='longitude']/@content'''
GET_INFO_XPATH_DESCRIPTION = '''//div[@class='zsg-lg-2-3 zsg-md-1-1 hdp-header-description']/div[@class='zsg-content-component']/div/text()'''
GET_INFO_XPATH_FOR_FACTS = '''//div[@class='fact-group-container zsg-content-component top-facts']/ul/li/text()'''
GET_INFO_XPATH_FOR_ADDITIONAL_FACTS = '''//div[@class='fact-group-container zsg-content-component z-moreless-content hide']/ul/li/text()'''
GET_SIMILAR_HOMES_FOR_SALE_XPATH = '''//ol[@id='fscomps']/li/div[@class='zsg-media-img']/a/@href'''

# Load user agents
USER_AGENTS_FILE = '../common/user_agents.txt'
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'rb') as uaf:
	for ua in uaf.readlines():
		if ua:
			USER_AGENTS.append(ua.strip()[1:-1:-1])
random.shuffle(USER_AGENTS)

#socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
#socket.socket = socks.socksocket


def build_url(url, path):
	if url[-1] is '/':
		url = url[:-1]
	return '%s/%s' % (url, path)

def getHeaders():
	ua = random.choice(USER_AGENTS)
	headers = {
		"Connection" : "close",
		"User-Agent" : ua,
	}
	return headers

def search_zillow(request_url, xpath):
	session_requests = requests.session()
	response = session_requests.get(request_url, headers=getHeaders())
	tree = html.fromstring(response.content)
	return tree.xpath(xpath)

""" Search properties by zipcode """
def search_zillow_by_zip(zipcode):
	request_url = '%s/%s' %(build_url(URL, SEARCH_FOR_SALE_PATH), str(zipcode))
	raw_result = search_zillow(request_url, SEARCH_XPATH_FOR_ZPID)
	return [x.replace('zpid_','') for x in raw_result]

""" Search properties by city and state """
def search__zillow_by_city_state(city, state):
	city_state = pathname2url('%s %s' % (city, state))
	request_url = '%s/%s' %(build_url(URL, SEARCH_FOR_SALE_PATH), city_state)
	raw_result = search_zillow(request_url, SEARCH_XPATH_FOR_ZPID)
	return [x.replace('zpid_','') for x in raw_result]


""" Get Property information by Zillow Property ID zpid """
def get_property_by_zpid(zpid):
	request_url = '%s/%s_zpid' % (build_url(URL, GET_PROPERTY_BY_ZPID_PATH), str(zpid))
	session_requests = requests.session()
	response = session_requests.get(request_url, headers=getHeaders())
#	print session_requests.get("http://www.google.com").text
#	print session_requests.get("http://icanhazip.com").text

	try:
		tree = html.fromstring(response.content)
		#print(tree)
	except Exception:
		return {}
	
	# Street address
	street_address = None
	try:
		street_address = tree.xpath(GET_INFO_XPATH_FOR_STREET_ADDR)
		if len(street_address) == 0:
			street_address = ''
		else:
			street_address = street_address[0].strip(', ')
	except Exception:
		pass

	# City, state and zipcode
	city_state_zipcode = None
	city = None
	state = None
	zipcode = None
	try:
		city_state_zipcode = tree.xpath(GET_INFO_XPATH_FOR_CITY_STATE_ZIP)
		if len(city_state_zipcode) == 0:
			city_state_zipcode = ''
		else:
			city_state_zipcode = city_state_zipcode[0].strip(', ')
			city = city_state_zipcode.split(',')[0].strip(', ')
			state = city_state_zipcode.split(',')[1].split(' ')[1].strip(', ')
			zipcode = city_state_zipcode.split(',')[1].split(' ')[2].strip(', ')
	except Exception:
		pass

	# Type: Condo, Twon house, simgle familty etc.	
	property_type = None
	# Bedroom
	bedroom = None
	# Bathroom
	bathroom = None
	#Size
	size = None
	try:	
		# Type: condo, town horse, single family etc.	
		property_type = tree.xpath(GET_INFO_XPATH_FOR_TYPE)[0]
	
		# Bedroom
		bedroom = float(tree.xpath(GET_INFO_XPATH_FOR_BEDROOM)[0].split(' ')[0])
		
		# Bathroom
		bathroom = float(tree.xpath(GET_INFO_XPATH_FOR_BATHROOM)[0].split(' ')[0])
	
		# Square feet
		size = int(tree.xpath(GET_INFO_XPATH_FOR_SIZE)[0].split(' ')[0].replace(',',''))
	except Exception:
		bedroom = 0
		bathroom = 0
		size = 0

	# Is for sale
	for_sale_text = None
	is_for_sale = False
	# Listed price
	list_price = None
	try:	
		# Is for sale
		for_sale_text = tree.xpath(GET_INFO_XPATH_FOR_SALE)
		r = re.compole('.+For Sale.+')
		is_for_sale = len(filter(r.match, for_sale_text)) > 0
	except Exception:
		is_for_sale = None

	try:	
		# Listed price
		list_price_raw = tree.xpath(GET_INFO_XPATH_LIST_FOR_PRICE)
		if(list_price_raw) > 0:
			list_price = float(list_price_raw[0].replace(',','').strip(' $'))
	except Exception:
		list_price = 'N/A'

	#Geo location
	latitude = None
	longitude = None
	try:	
		# Geo locations
		latitude = float(tree.xpath(GET_INFO_XPATH_FOR_LATITUDE)[0])
		longitude = float(tree.xpath(GET_INFO_XPATH_FOR_LONGITUDE)[0])
	except Exception:
		pass	

	# Image
	image_url = None
	try:	
		# Image
		image_url = re.compile(IMAGE_URL_REGEX_PATTERN)
		result = r.search(response.content)
		image_url = result.group(1)
	except Exception:
		pass


	# Description
	description = None
	# Basic facts
	facts = None
	# Additional facts
	additional_facts = None
	try:
		# Description
		description = tree.xpath(GET_INFO_XPATH_DESCRIPTION)

		# Basic facts
		facts = tree.xpath(GET_INFO_XPATH_FOR_FACTS)

		# Additional facts
		additional_facts = tree.xpath(GET_INFO_XPATH_FOR_ADDITIONAL_FACTS)
	except Exception:
		pass
		
	return {
		'zpid': zpid,
		'street_address': street_address,
		'city': city,
		'state': state,
		'zipcode': zipcode,
		'property_type': property_type,
		'bedroom': bedroom,
		'bathroom': bathroom,
		'size': size,
		'latitude': latitude,
		'longitude': longitude,
		'is_for_sale': is_for_sale,
		'list_price': list_price,
		'image_url': image_url,
		'description': description,
		'facts': facts,
		'additional_facts': additional_facts,
		}	
 
""" Get similar homes for sale """
def get_similar_homes_for_sale_by_id(zpid):
	request_url = '%s/%s_zpid' % (build_url(URL, GET_SIMILAR_HOMES_FOR_SALE_PATH), str(zpid))
	raw_result = search_zillow(request_url, GET_SIMILAR_HOMES_FOR_SALE_XPATH)
	return [re.search(SIMILAR_HOMES_ZPID_REGEX_PATTERN, x).group(1) for x in raw_result]

""" Get properties information by zipcode """
def get_properties_by_zipcode(zipcode):
	zpids = search_zillow_by_zip(ziocode)
	return [get_property_by_zpid(zpid) for zpid in zpids]

""" Get properties information by city and state """
def get_properties_by_city_state(city, state):
	zpids = search_zillow_by_city_state(city, state)
	return [get_property_by_zpid(zpid) for zpid in zpids]

