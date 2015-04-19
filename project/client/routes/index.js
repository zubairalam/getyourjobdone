var router = require('express').Router(),
    core = require('./core');


module.exports = (function () {
    'use strict';

    router.use(core);
    return router;
})();