var express = require('express'),
    router = express.Router(),
    uploader = require('../controllers/upload_profile_photo');

module.exports = (function () {
    router.route('/profile-wizard/upload')
        .post(uploader.upload);
    return router;
})();
