var User = require('../models/user'),
    mailer = require('../config/email'),
    format = require('../helpers/string.format');

exports.authenticateUser = function (req, res) {
    var email = req.body.email.trim();
    var password = req.body.password.trim();
    User.findOne({email: email}, function (err, user) {
        if (err)
            return res.json({"message": err});
        if (!user)
            return res.json({"message": "user does not exist"});

        if (!user.validPassword(password))
            return res.json({"message": "invalid credentials"});

        // need to return user_id + accesstoken + expiry time ttl e.g 1hr
        // update last login time.
        return res.json(user);
    });

};

exports.sendForgottenPasswordReminder = function (req, res) {
    var email = req.body.email.trim();
    User.findOne({email: email}, function (err, user) {
        if (err)
            return res.json({"message": err});

        if (!user)
            return res.json({"message": "user does not exist"});

        var mailOptions = {
            from: 'firethoughts Developers <developers@firethoughts.com>',
            to: email,
            subject: 'Your password reminder, {0}'.format(user.firstName),
            text: 'Please click on this link to reset your password: {0}'.format(user.token),
            html: '<b>Please click on this link to reset your password: {0} ✔</b>'.format(user.token)
        };
        mailer.sendMail(mailOptions, function (error, info) {
            if (error) {
                console.log(error);
            } else {
                console.log('Message sent: ' + info.response);
            }
        });

        return res.json(user);

    });
};
