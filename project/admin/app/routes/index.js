var express = require('express');

var genericRoute = require('./generic');

module.exports = (function () {
    'use strict';
    var router = express.Router();
    router.use(genericRoute);

    // put in the end cause of the 404/500 middleware
    // 404 catch all handler middleware
    router.use(function (req, res, next) {
        res.status(404);
        res.render('404');
    });
    //500 error handler middleware
    router.use(function (req, res, next) {
        res.status(500);
        res.render('500');
    });

    return router;
})();