var express = require('express');
var genericController = require('../controllers/generic');

module.exports = (function () {

    var router = express.Router();
    router.route('/')
        .get(genericController.getHome);

    return router;
})();
