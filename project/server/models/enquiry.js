var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    name: {type: String, es_indexed: true},
    email: {type: String, es_indexed: true},
    subject: {type: String, es_indexed: true},
    description: {type: String, es_indexed: true}
});

schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});

var object = module.exports = mongoose.model('Enquiry', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' enquiries!');
});
stream.on('error', function (err) {
    console.log(err);
});
