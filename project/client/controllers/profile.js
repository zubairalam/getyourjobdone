var context = require('../helpers'),
    _str = require('underscore.string'),
    uuid = require('node-uuid'),
    RestClient = require('node-rest-client').Client,
    restcli = new RestClient();


exports.profileWizardController = function (req, res) {
    'use strict';

    context.injectSetting(req, res, 'profile/index', { title: 'Profile Wizard' });
};

exports.companyProfileWizardController = function (req, res) {
    'use strict';

    context.injectSetting(req, res, 'profile/company-profile', { title: 'Company Profile Wizard' });
};


/* ToDo: change url in address bar :: use res.redirect with context */
exports.verifyEmail = function (req, res) {
    'use strict';
    var token = req.param('token'),
        args = {
            data: { token: token },
            headers: {"Content-Type": "application/json"}
        };
    restcli.post('http://localhost:5000/api/v1/verify-email', args, function (data, response) {
        var result = JSON.parse(data)
        console.log(result, result.isVerified);
        if (undefined !== result) {
            if (!result.isVerified) {
                /* email not verified, token is not correct */
                context.injectSetting(req, res, 'auth/signup', { title: 'Sign up', isEmailVerified: false });
            } else {
                /* email is verified */
                context.injectSetting(req, res, 'profile/index', { title: 'Profile Wizard', isEmailVerified: true });
            }
        } else {
            /* email not verified, some error */
            context.injectSetting(req, res, 'auth/signup', { title: 'Sign up', isEmailVerified: false });
        }
    });

};

