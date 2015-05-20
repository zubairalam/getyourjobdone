var mongoose = require('mongoose'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    /*
        Essential and most common available data about a job opening
    */
    title: {type: String, required: true},
    url: {type: String, index: true, unique: true, required: true},
    description: {type: String},

    /*
        might be available or have to filter these information
    */

    keyskills: {type: String},
    salary: {type: String},
    year_of_experiences: {type: String},
    location: {type: String},
    company: {type: String},
    tags: [{type: String}]
});

schema.plugin(timestamps);

var object = module.exports = mongoose.model('Job', schema);
