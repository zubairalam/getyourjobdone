var express = require('express'),
    router = express.Router(),
    setting = require('../controllers/setting');

module.exports = (function () {
    router.route('/settings/')
        .get(setting.getSettings)
        .post(setting.setSetting);

    router.route('/settings/:key')
        .get(setting.getSetting)
        .delete(setting.deleteSetting);

    return router;
})();
