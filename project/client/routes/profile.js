var express = require('express'),
    router = express.Router(),
    profile = require('../controllers/profile');

module.exports = (function () {

    router.route('/profile-wizard')
        .get(profile.profileWizardController);

    router.route('/verify-email/:token')
        .get(profile.verifyEmail);

    router.route('/cp-wizard')
        .get(profile.companyProfileWizardController);



    return router;
})();
