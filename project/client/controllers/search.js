var context = require('../helpers');


exports.searchController = function (req, res) {
    context.injectSetting(req, res, 'search/index', { title: 'Search' });
};

exports.searchController2 = function (req, res) {
    context.injectSetting(req, res, 'search/index_infy', { title: 'Search' });
};