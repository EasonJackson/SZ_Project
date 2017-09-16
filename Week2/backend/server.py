import os
import pyjsonrpc
import sys
import json
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..','common'))

from bson.json_util import dumps

import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

PROPERTY_TABLE_NAME = 'property'

class RequestHandler(pyjsonrpc.HttpRequestHandler):
	"""Test method"""
	@pyjsonrpc.rpcmethod
	def add(self, a, b):
		print "add gets called with %d and %d" % (a, b)
		return a + b

	@pyjsonrpc.rpcmethod
	def searchArea(self, query):
		res = []
		if query.isdigit():
			db = mongodb_client.getDB()
			res = db[PROPERTY_TABLE_NAME].find({'zipcode': query})
			res = json.loads(dumps(res))
		else:
			city = query.split(',')[0].strip()
			state = query.split(',')[1],strip()
			#TODO search in DB
		return res

http_server = pyjsonrpc.ThreadingHttpServer(
	server_address = (SERVER_HOST, SERVER_PORT),
	RequestHandlerClass = RequestHandler
)

print "Starting HTTP server..."
print "Lisntening on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
