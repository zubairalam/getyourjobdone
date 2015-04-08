var express = require('express'),
    router = express.Router(),
    dashboard = require('../controllers/dashboard');

module.exports = (function () {
    router.route('/dashboard')
        .get(dashboard.overViewController);
    return router;
})();

