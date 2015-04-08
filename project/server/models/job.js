var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
    monguurl = require('monguurl'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    name: {type: String, es_indexed: true},
    description: {type: String, es_indexed: true},
    category: {
        type: String,
        enum: ['Freelance', 'Part-Time', 'Full-Time', 'Internship', 'Volunteer']
    },
    education: {
        type: String,
        enum: ['SC', 'HSC', 'Diploma', 'Degree', 'Masters', 'Doctorate']
    },
    experience: {
        type: String,
        enum: ['Junior', 'Middle', 'Senior', 'Expert']
    },
    visa: {
        type: String,
        enum: ['Local', 'SADC', 'Visa']
    },
    presence: {
        type: String,
        enum: ['Remote', 'Office', 'Travel']
    },

    salary: Number,
    salaryFrequency: {
        type: String,
        enum: ['Day', 'Week', 'Month', 'Year']
    },
    salaryNegotiable: {
        type: Boolean,
        default: true
    },
    slug: {
        type: String,
        index: {unique: true}
    },
    recruiter: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    company: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Company'
    },
    location: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Location'
    },
    benefits: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Benefit'
    }],

    skills: [{
        name: String,
        ratio: Number
    }],
    closingDate: {
        type: Date,
        default: Date.now
    },
    startDate: Date,
    languages: [{
        language: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Language'
        },
        how: Number
    }],
    workDays: [{
        type: String,
        enum: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }],
    startTime: Number,
    endTime: Number
});

schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});
schema.plugin(monguurl({source: 'name', target: 'slug'}));

var object = module.exports = mongoose.model('Job', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' jobs!');
});
stream.on('error', function (err) {
    console.log(err);
});
