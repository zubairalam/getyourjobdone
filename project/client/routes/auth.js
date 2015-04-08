var router = require('express').Router(),
    auth = require('../controllers/auth');

module.exports = (function () {

    router.route('/signup')
        .get(auth.signUpController);

    router.route('/login')
        .get(auth.loginController);

    router.route('/logout')
        .get(auth.logoutController);

    router.route('/forgot')
        .get(auth.forgotPasswordController);

    return router;
})();
