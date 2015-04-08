var context = require('../helpers');


exports.overViewController = function (req, res) {
    context.injectSetting(req, res, 'dashboard/overview', { title: 'Overview' });
};

