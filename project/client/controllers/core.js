var context = require('../helpers');

exports.aboutController = function (req, res) {
    context.injectSetting(req, res, 'core/about', {title: 'About Us'});
};

exports.advertiseController = function (req, res) {
    context.injectSetting(req, res, 'core/advertise', {title: 'Advertise with us'});
};

exports.careersController = function (req, res) {
    context.injectSetting(req, res, 'core/careers', {title: 'Careers'});
};

exports.faqController = function (req, res) {
    context.injectSetting(req, res, 'core/faq', {title: 'FAQ'});
};

exports.homeController = function (req, res) {
    context.injectSetting(req, res, 'core/home', {title: 'Home'});
};

exports.pricingController = function (req, res) {
    context.injectSetting(req, res, 'core/pricing', {title: 'Pricing'});
};

exports.privacyController = function (req, res) {
    context.injectSetting(req, res, 'core/privacy', {title: 'Privacy Policy'});
};

exports.securityController = function (req, res) {
    context.injectSetting(req, res, 'core/security', {title: 'Cookies and Security'});
};

exports.supportController = function (req, res) {
    context.injectSetting(req, res, 'core/support', {title: 'Support'});
};

exports.termsController = function (req, res) {
    context.injectSetting(req, res, 'core/terms', {title: 'Terms & Conditions'});
};
