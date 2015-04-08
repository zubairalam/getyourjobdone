var context = require('../helpers');

exports.error404Controller = function (req, res) {
    res.status(404);
    context.injectSetting(req, res, '404', { title: 'Oops 404 Error' });
};

exports.error500Controller = function (req, res) {
    res.status(500);
    context.injectSetting(req, res, '500', { title: 'Oops 500 Error' });
};
