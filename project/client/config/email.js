var nodemailer = require('nodemailer');

// create reusable transporter object using SMTP transport

var transporter = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: 'developers@xeontek.com',
        pass: 'pythongeeks'
    }
});
module.exports = transporter;
