var mongoose = require('mongoose-q')(require('mongoose')),
    mongoosastic = require('mongoosastic'),
    timestamps = require('mongoose-time');

var schema = new mongoose.Schema({
    date: Date,
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    action: String,
    detail: mongoose.Schema.Types.Mixed
});

schema.plugin(timestamps);
schema.plugin(mongoosastic, {index: 'jps', hydrate: true, hydrateOptions: {lean: true}});

var object = module.exports = mongoose.model('Activity', schema),
    stream = object.synchronize(),
    count = 0;

stream.on('data', function (err, doc) {
    count++;
});
stream.on('close', function () {
    console.log('indexed ' + count + ' activities!');
});
stream.on('error', function (err) {
    console.log(err);
});
