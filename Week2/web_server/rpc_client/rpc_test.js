var client = require('./rpc_client');

//client.add(1, 2, function(response) {
//	console.log("1 + 2 =" + response);
//});

client.searchArea('94000', function(response) {
	console.log('94000 - ' + response);
});
