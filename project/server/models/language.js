var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
    monguurl = require('monguurl'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    name: {type: String, es_indexed: true},
    alpha2: String,
    bibliographic: String,
    terminology: String,
    slug: {
        type: String,
        index: {unique: true}
    }
});


schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});
schema.plugin(monguurl({source: 'name', target: 'slug'}));

var object = module.exports = mongoose.model('Language', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' languages!');
});
stream.on('error', function (err) {
    console.log(err);
});
