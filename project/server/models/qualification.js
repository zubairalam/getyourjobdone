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
    }
});

schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});
schema.plugin(monguurl({source: 'name', target: 'slug'}));

var object = module.exports = mongoose.model('Qualifcation', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' qualifications!');
});
stream.on('error', function (err) {
    console.log(err);
});
