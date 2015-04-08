var User = require('../models/user'),
    mongoose = require('mongoose'),
    Location = require('../models/location'),
    Company = require('../models/company'),
    Industry = require('../models/industry'),
    mailer = require('../config/email'),
    crypto = require('crypto'),
    format = require('../helpers/string.format');

exports.createProfile = function (req, res) {
    var address = req.body.address,
        gender = req.body.gender,
        current_job_status = req.body.current_job_status,
        skills = req.body.skills,
        token = req.body.token;

    User.findOne({token: token}, function (err, user) {
        if (err || !user) {
            return res.json({message: 'some error while creating individual profile'});
        }
        var location = new Location({
            address: address
        });

        location.save(function (err) {
            user.location = location._id;
        });
        
        user.gender = gender;
        user.currentJobStatus = current_job_status;
        
        skills.forEach(function (skill) {
            user.skills_set.push(skill);
            console.log(skill);
        });

        user.save(function (err) {
            console.log(user.skills_set, user.skills_set.length);
            return res.json(user);
        });
    });
};


exports.createCompanyProfile = function (req, res) {
    var token = req.body.token,
        address = req.body.address,
        name = req.body.name,
        website = req.body.website,
        companyType = req.body.companyType,
        companySize = req.body.companySize,
        hiring = req.body.hiring,
        industry = req.body.industry, // industry == industry._id a string
        services = req.body.services;
    
        console.log(industry, "<====");
    
    User.findOne({token: token}, function (err, user) {
        if (err) {
            res.json({message: 'error while searching user'});
        }

        if (!user) {
            res.json({message: 'user not found'});
        }
        
        Company.findOne({representative: user._id}, function (err, company) {
            if (err) {
                res.json({message: 'error while searching a company'});
            }
            
            if (!company) {
                var location = new Location({
                    address: address
                });   

                location.save(function (err) {
                    Industry.findOne({_id: industry}, function (err, industry) {
                        if (err || !industry) {
                            return res.json({message: 'industry not found'});
                        }
                        var company = new Company({
                            name: name,
                            category: companyType,
                            size: companySize,
                            website: website,
                            hiring: hiring,
                            services: services,
                            representative: user._id,
                            locations: location._id,
                            industries: industry._id
                        });

                        company.save(function (err) {
                            if (err) {
                                return res.json({message: 'error while saving company'});
                            }
                            res.status(200);
                            return res.json({message: 'company saved'});
                        }); 

                    });

                }); 
            }
            
            return res.json({message: 'company exists'});
            
        });       
        
    });
    
};


exports.verifyEmail = function (req, res) {
    'use strict';
    /* post http://localhost:5000/api/v1/ */
    var token = req.body.token;
    User.findOne({token:token}, function (err, user) {
        if (err || !user){
            return res.json({isVerified: false})
        }
        
        console.log(user);
        
        user.token = crypto.randomBytes(32).toString('hex');
        user.isEmailVerified = true;
        user.save(function (err) {
            return res.json({isVerified: true});
        });
    });
};

exports.sendEmailVerification = function (req, res) {
    'use strict';
    
    var token = req.body.token;
    User.findOne({token:token}, function (err, user) {
        if (err || !user){
            res.json({message: 'error'})
        }
        user.sendEmailVerification();
        res.json({message: 'email sent'});
    });
};
