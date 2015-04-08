var express = require('express'),
    router = express.Router(),
    profile = require('../controllers/profile'),
    companyProfile = require('../controllers/companyProfile');

module.exports = (function () {
    router.route('/create-profile')
        .post(profile.createProfile);
    
    // router.route('/create-company-profile')
    //     .post(profile.createCompanyProfile);
    
    router.route('/verify-email')
        .post(profile.verifyEmail);
    
    router.route('/send-email-verification')
        .post(profile.sendEmailVerification);
    
    router.route('/create-company-profile')
        .post(companyProfile.profile);
    return router;
})();
