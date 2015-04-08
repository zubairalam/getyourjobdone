var express = require('express'),
    router = express.Router(),
    auth = require('../controllers/auth');

module.exports = (function () {
    router.route('/auth/local/login')
        .post(auth.authenticateUser);

    router.route('/auth/local/forgot')
        .post(auth.sendForgottenPasswordReminder);

    return router;
})();
