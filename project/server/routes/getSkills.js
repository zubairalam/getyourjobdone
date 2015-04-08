var express = require('express'),
    router = express.Router(),
    getSkills = require('../controllers/getSkills').getSkills;

module.exports = (function () {
    router.route('/get_skills')
        .get(getSkills);
    return router;
})();
