var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
    monguurl = require('monguurl'),
    timestamps = require('mongoose-time'),
    crypto = require('crypto'),
    bcrypt = require('bcrypt-nodejs'),
    gravatar = require('../helpers/gravatar'),
    format = require('../helpers/string.format'),
    email = require('../config/email');


var schema = new mongoose.Schema({
    email: {
        type: String,
        unique: true,
        es_indexed: true,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    accountType: {
        type: String,
        required: true
    },
    token: {
        type: String,
        unique: true
    },
    lastLogin: {
        type: Date,
        default: Date.now
    },
    isAdmin: {
        type: Boolean,
        default: false
    },
    isEmailVerified: {
        type: Boolean,
        default: false
    },
    isSMSVerified: {
        type: Boolean,
        default: false
    },
    firstName: {
        type: String,
        es_indexed: true,
        required: true
    },
    middleName: {
        type: String,
        es_indexed: true
    },
    lastName: {
        type: String,
        es_indexed: true,
        required: true
    },
    salutation: {
        type: String
    },
    bio: {
        type: String,
        es_indexed: true
    },
    location: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Location'
    },
    gender: {
        type: String
    },
    picture: {
        type: String
    },
    video: {
        type: String
    },
    mobile: {
        type: String
    },
    phone: {
        type: String
    },
    fax: {
        type: String
    },
    dateOfBirth: {
        type: Date
    },
    skills_set: [String],
    profession: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Profession'
    }],
    currentJobStatus: {
        type: String
    },
    contacts: [{
        user: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User'
        },
        relationship: {
            type: String,
            enum: ['Online', 'Friend', 'Colleague', 'Acquaintance', 'Referral']
        }
    }],
    languages: [{
        language: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Language'
        },
        strength: Number
    }],
    skills: [{
        skill: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Skill'
        },
        strength: Number
    }],
    hobbies: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Hobby'
    }],
    qualifications: [{
        qualification: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Qualification'
        },
        institution: {type: String, es_indexed: true},
        notes: String,
        start: Date,
        end: Date
    }],
    experience: [{
        company: {type: String, es_indexed: true},
        notes: String,
        start: Date,
        end: Date
    }],
    activities: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Activity'
    }],
    slug: {
        type: String,
        index: {unique: true}
    }

});

schema.virtual('fullName').get(function () {
    if (this.middleName)
        return '{0} {1} {2}'.format(this.firstName, this.middleName, this.lastName);
    return '{0} {1}'.format(this.firstName, this.lastName);
});

schema.methods.getAvatar = function() {
    if (!this.picture)
        return gravatar.imageUrl(this.email);
    return this.picture;
};

schema.methods.generateHash = function (password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

schema.methods.validPassword = function (password) {
    return bcrypt.compareSync(password, this.password);
};


schema.pre("save", function (next) {
    this.password = this.generateHash(this.password);
    this.token = crypto.randomBytes(32).toString('hex');
    next();
});

/*schema.post('save', function (doc) {
    var mailOptions = {
        from: 'firethoughts Developers <developers@firethoughts.com>',
        to: this.email,
        subject: 'Welcome to firethoughts, {0}'.format(this.firstName),
        text: 'Hello {0}'.format(this.fullName),
        html: '<b>Hello {0}, please visit this <a href="http://localhost:3000/verify-email/{1}">this</a> link to verify your email id.</b>'.format(this.fullName, this.token)
    };
    email.sendMail(mailOptions, function (error, info) {
        if (error) {
            console.log(error);
        } else {
            console.log('Message sent: ' + info.response);
        }
    });
});*/

schema.methods.sendEmailVerification = function () {
    var mailOptions = {
        from: 'firethoughts Developers <developers@firethoughts.com>',
        to: this.email,
        subject: 'Welcome to firethoughts, {0}'.format(this.firstName),
        text: 'Hello {0}'.format(this.fullName),
        html: '<b>Hello {0}, please visit this <a href="http://localhost:3000/verify-email/{1}">this</a> link to verify your email id.</b>'.format(this.fullName, this.token)
    };
    email.sendMail(mailOptions, function (error, info) {
        if (error) {
            console.log(error);
        } else {
            console.log('Message sent: ' + info.response);
        }
    });
};


schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});
schema.plugin(monguurl({source: 'fullName', target: 'slug'}));


var object = module.exports = mongoose.model('User', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' users!');
});
stream.on('error', function (err) {
    console.log(err);
});
