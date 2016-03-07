var express = require('express');
var router = express.Router();

var Firebase = require('firebase');
var myFirebaseRef = new Firebase('https://ntuaf-hand.firebaseio.com/');

myFirebaseRef.authWithCustomToken('9SxGgVAA60TXNHGIwBx72PP2kGOpBmQrpF7kcd9o', function(error, authData) {
  if (error) {
    console.log("Authentication Failed!", error);
  } else {
    console.log("Authenticated successfully with payload:", authData);
  }
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/photos/status', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/photos/add', function(req, res, next) {
  var filename = req.query.filename;
  var photosRef = myFirebaseRef.child('photos/' + filename);
  var onComplete = function(error) {
    if (error) {
      console.log('Synchronization failed');
      res.json({status: 'error'});
    } else {
      console.log('Synchronization succeeded');
      res.json({status: 'success'});
    }
  };

  photosRef.set({
      hits: 0
  }, onComplete);
});

module.exports = router;
