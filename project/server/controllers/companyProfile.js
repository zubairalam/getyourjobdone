var User = require('../models/user'),
    mongoose = require('mongoose'),
    ObjectId = require('mongoose').Types.ObjectId,
    Location = require('../models/location'),
    Company = require('../models/company'),
    Industry = require('../models/industry'),
    mailer = require('../config/email'),
    crypto = require('crypto'),
    format = require('../helpers/string.format')
    RSVP = require('rsvp');

var user,
 	industry,
 	location;

var companyExistsPromise = function (user_id) {
	var promise = new RSVP.Promise(function (resolve, reject) {
		Company.findOne({ representative: new ObjectId(user_id) })
			.exec(function (err, company) {
				if (company) {
					console.log('company is found');
					return reject({message: 'company is already there'});
				}
				console.log('company not found');
				resolve({message: 'company not found'});
			});
	});
	return promise;
};

var getUserPromise = function (user_id) {
	return new RSVP.Promise(function (resolve, reject) {
		User.findOne({ _id: new ObjectId(user_id) }, function (err, user) {
			if (err || !user) {
				return reject({message: 'user not found'});
			}
			resolve(user);
		});
	});
};

var getIndustryPromise = function (industry_id) {
	return new RSVP.Promise(function (resolve, reject) {
		Industry.findOne({_id: new ObjectId(industry_id)}, function (err, industry) {
			if (err || !industry) {
				return reject({message: 'industry can not be found'});
			}
			resolve(industry)
		});
	});
};

var saveLocationPromise = function (address) {
	return new RSVP.Promise(function (resolve, reject) {
		var location = new Location({
		    address: address
		});

		location.save(function (err) {
			if (err) {
				return reject({message: 'location can not saved'});
			}
			resolve(location);
		});
	});
};

var saveCompanyPromise = function (obj) {
	return new RSVP.Promise(function (resolve, reject) {
		var company = new Company({
		    name: obj.name,
		    category: obj.companyType,
		    size: obj.companySize,
		    website: obj.website,
		    hiring: obj.hiring,
		    services: obj.services,
		    representative: obj.user._id,
		    locations: obj.location._id,
		    industries: obj.industry._id
		});

		company.save(function (err) {
			if (err) {
				return reject({message: 'company can not be saved'});
			}
			resolve(company);
		});
	});
};


exports.profile = function (req, res) {
	var user_id = req.body.user_id,
        address = req.body.address,
        name = req.body.name,
        website = req.body.website,
        companyType = req.body.companyType,
        companySize = req.body.companySize,
        hiring = req.body.hiring,
        industry_id = req.body.industry,
        services = req.body.services;

	return companyExistsPromise(user_id)
		.then(function (message) {
			return getUserPromise(user_id);
		})
		.then(function (userObject) {
			user = userObject;
			return getIndustryPromise(industry_id);
		})
		.then(function (industryObject) {
			industry = industryObject;
			return saveLocationPromise(address);
		})
		.then(function (locationObject) {
			location = locationObject;
			return saveCompanyPromise({ 
				user: user,
		        address: address,
		        name: name,
		        website: website,
		        companyType: companyType,
		        companySize: companySize,
		        hiring: hiring,
		        industry: industry,
		        services: services,
		        location: location
				});
		})
		.then(function (companyObject) {
			return res.json(companyObject);
		}, function (error) {
			return res.json(error);
		});
};
