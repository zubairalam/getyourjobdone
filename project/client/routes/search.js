var express = require('express'),
    router = express.Router(),
    search = require('../controllers/search');

module.exports = (function () {

    router.route('/search')
        .get(search.searchController);

    router.route('/search2')
        .get(search.searchController2);

    return router;
})();