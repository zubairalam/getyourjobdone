var router = require('express').Router(),
    auth = require('./auth'),
    core = require('./core'),
    dashboard = require('./dashboard'),
    profile = require('./profile'),
    search = require('./search'),
    error = require('../controllers/error');


module.exports = (function () {
    'use strict';

    router.use(auth);
    router.use(core);
    router.use(dashboard);
    router.use(profile);
    router.use(search);
    router.use(error.error404Controller);
    router.use(error.error500Controller);
    return router;
})();