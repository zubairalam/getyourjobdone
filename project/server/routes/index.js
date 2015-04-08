var express = require('express'),
    moment = require('moment'),
    router = express.Router(),
    restify = require('express-restify-mongoose');

exports.restifyRoutes = (function (app) {
    'use strict';
    restify.serve(app, require('../models/activity'));
    restify.serve(app, require('../models/benefit'));
    restify.serve(app, require('../models/blogCategory'));
    restify.serve(app, require('../models/blogPost'));
    restify.serve(app, require('../models/company'));
    restify.serve(app, require('../models/country'));
    restify.serve(app, require('../models/course'));
    restify.serve(app, require('../models/emailTemplate'));
    restify.serve(app, require('../models/enquiry'));
    restify.serve(app, require('../models/hobby'));
    restify.serve(app, require('../models/industry'));
    restify.serve(app, require('../models/job'));
    restify.serve(app, require('../models/language'));
    restify.serve(app, require('../models/location'));
    restify.serve(app, require('../models/log'));
    restify.serve(app, require('../models/package'));
    restify.serve(app, require('../models/profession'));
    restify.serve(app, require('../models/qualification'));
    restify.serve(app, require('../models/skill'));
    restify.serve(app, require('../models/user'));
    return restify;
});


exports.customRoutes = (function () {
    'use strict';
    router.use(function (req, res, next) {
        console.log('Request made: %s - %s : %s', req.url, moment().format('MMMM Do YYYY, h:mm:ss a'), res.statusCode);
        next();
    });

    router.get('/', function (req, res) {
        res.json({message: 'Welcome to firethoughts API!'});
    });

    router.use(require('./auth'));
    router.use(require('./setting'));
    router.use(require('./location'));
    router.use(require('./upload_profile_photo'));
    router.use(require('./profile'));
    router.use(require('./getSkills'));
    return router;
})();
