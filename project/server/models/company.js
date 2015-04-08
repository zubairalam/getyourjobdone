var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
   monguurl = require('monguurl'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    name: {type: String, es_indexed: true},
    description: {type: String, es_indexed: true},
    slug: {
        type: String,
        index: {unique: true}
    },
    website: {type: String},
    hiring: {type: String},
    services: {type: Object},
    representative: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    established: Number,
    size: {
        type: String,
        enum: ['Small', 'Medium', 'Large']
    },
    category: {
        type: String,
        enum: ['Private', 'Public', 'Charity', 'Government']
    },
    industries: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Industry'
    }],
    locations: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Location'
    }]
});

schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});
schema.plugin(monguurl({source: 'name', target: 'slug'}));

var object = module.exports = mongoose.model('Company', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' companies!');
});
stream.on('error', function (err) {
    console.log(err);
});

