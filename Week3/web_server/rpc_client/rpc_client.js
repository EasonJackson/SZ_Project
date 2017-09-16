var jayson = require('jayson');

// create a client connected to backend server
var client = jayson.client.http({
	hostname: 'localhost',
	port: 4040
});

// Test RPC method add()
function add(a, b, callback) {
	client.request('add',[a, b], function(err, error, response){
		if(err) throw err;
		console.log(response);
		callback(response);
	});
}

// Search property using address and city/state or zip code
function searchByAddress(address, cotustatezip, callback) {
	client.request('searchByAddress', [address, citystatezip], function(err, error, response) {
		if (err) throw err;
		console.log(response);
		callback(response);
	});
}

// Search properties using zip code
function searchAreaByZip(zipcode, callback) {
	client.request('searchAreaByZip', [zipcode], function(err, error, response) {
		if (err) throw err;
		console.log(response);
		callback(response);
	});
}

// Searh properties using city and state
function searchAreaByCityState(city, state, callback) {
	client.request('searchAreaByCityState', [city, state], function(err, error, response) {
		if (err) throw err;
		console.log(response);
		callback(response);
	});
}

// Search properties
function searchArea(query, callback) {
	client.request('searchArea', [query], function(err, error, response) {
		if(err) throw err;
		console.log(response);
		callback(response);
	});
}

// Get property details by Zillow property ID (zpid)
function getDetailsByZpid(zpid, callback) {
	client.request('getDetailsByZpid', [zpid], function(err, error, response) {
		if(err) throw err;
		console.log(response);
		callback(response);
	});
}

module.exports = {
	add: add,
	searchArea: searchArea,
	searchByAddress: searchByAddress,
	searchAreaByZip: searchAreaByZip,
	searchAreaByCityState: searchAreaByCityState,
	getDetailsByZpid: getDetailsByZpid,
};
