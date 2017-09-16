var express = require('express');
var router = express.Router();
var User = require('../model/user');
var passwordHash = require('password-hash');

var session = require('client-sessions');

TITLE = 'SmartZillow';

/* GET home page. */
router.get('/', function(req, res, next) {
  var user = checkLoggedIn(req, res);
  res.render('index', { title: TITLE, logged_in_user: user });
});


/* Register */
router.get('/register', function(req, res, next) {
	res.render('register', { title: TITLE})
});

router.post('/register', function(req, res, next) {
	var email = req.body.email;
	var password = req.body.password;
	var hashedPassword = passwordHash.generate(password);

	User.find({email: email}, function(err, users) {
		if(err) throw err;

		// User name/email already used.
		if(users.length > 0) {
			console.log("User found for: " + email);
			res.render('register', {
				title: TITLE,
				message: 'Email is already used. Pleas pick a new one. Or<a href="/login">Login</a>'
			});
		} else {
			var newUser = User({
				email: email,
				password: hashedPassword,
			});
			// Save the user.
			newUser.save(function(err) {
				if(err) throw err;
				console.log('User created!');
				req.session.user = email;
				res.redirect('/');
			});
		}
	});
});

/* Login. */
router.get('/login', function(req, res, next) {
  res.render('login', { title: TITLE });
});

router.post('/login', function(req, res, next) {
	var email = req.body.email;
	var password = req.body.password;

	User.find({email: email}, function(err, users) {
		console.log(users);
		if(err) throw err;

		//User not found.
		if(users.length == 0) {
			res.render('login', {
				title: TITLE,
				message: "User not found. Or <a href='/register'>register</a>"

				//Promote to register
			});
			console.log("Not found");
		} else {
			//User found.
			var user = users[0];
			if(passwordHash.verify(password, user.password)) {
				console.log(user);
				req.session.user = user.email;
				res.redirect('/');
			} else {
				res.render('login', {
					title: TITLE,
					message: "Password incorrect. Or <a href='/register'>register</a>"
				});
			}
		}
	});
});

/* Logout*/
router.get('/logout', function(req, res) {
	req.session.reset();
	res.redirect('/');
});

function checkLoggedIn(req, res) {
	//Check if session exists
	if(req.session && req.session.user) {
		return req.session.user;
	}
	return null;
}


module.exports = router;
