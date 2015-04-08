var context = require('../helpers');


exports.loginController = function (req, res) {
    context.injectSetting(req, res, 'auth/login', { title: 'Login' });
};

exports.logoutController = function (req, res) {
    req.logout();
    res.redirect('/');
};

exports.signUpController = function (req, res) {
    context.injectSetting(req, res, 'auth/signup', { title: 'Sign up' });
};

exports.forgotPasswordController = function (req, res) {
    context.injectSetting(req, res, 'auth/forgot', { title: 'Forgot Password' });
};

exports.dashboardController = function (req, res) {
    context.injectSetting(req, res, 'auth/dashboard', { title: 'My Dashboard' });
};
