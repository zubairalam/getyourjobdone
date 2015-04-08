var path = require('path'),
	redis = require('../config/redis'),
    fs = require('fs'),
    os = require('os'),
    inspect = require('util').inspect,
    Busboy = require('busboy');



exports.upload = function (req, res, next) {

	var busboy = new Busboy({ headers: req.headers });

	var token, image;


	busboy.on('file', function(fieldname, file, filename, encoding, mimetype) {

	  var saveTo = path.join(__dirname, "../staticfiles/uploads/images/profile/"+path.basename(filename));
	  file.pipe(fs.createWriteStream(saveTo));
	  
	  
	  file.on('data', function(data) {
	  });

	  file.on('end', function() {
	  	
	  });
	});
	
	busboy.on('field', function(fieldname, val, fieldnameTruncated, valTruncated) {
		if (fieldname==="token")
			token=val;
		if (fieldname==="flowFilename")
			image=val;
	});
	
	busboy.on('finish', function() {
		// res.status(200);
		redis.hset(['upload_images', token, image], function (err, value) {
		    if (err) {
		        console.log(err);
		    }
		});
		res.json({'message': 'uploaded'});
		res.end();
	});
	
	req.pipe(busboy);
};

