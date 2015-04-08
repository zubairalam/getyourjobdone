var express = require('express'),
    router = express.Router(),
    core = require('../controllers/core');

module.exports = (function () {

    router.route('/')
        .get(core.homeController);

    router.route('/about')
        .get(core.aboutController);

    router.route('/advertise')
        .get(core.advertiseController);

    router.route('/careers')
        .get(core.careersController);

    router.route('/faq')
        .get(core.faqController);

    router.route('/pricing')
        .get(core.pricingController);

    router.route('/privacy')
        .get(core.privacyController);

    router.route('/terms')
        .get(core.termsController);

    router.route('/security')
        .get(core.securityController);

    router.route('/support')
        .get(core.supportController);

    return router;
})();
