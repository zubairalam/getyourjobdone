var express = require('express'),
    router = express.Router(),
    core = require('../controllers/core');

module.exports = (function () {

    router.route('/')
        .get(core.homeController);

    return router;
})();
