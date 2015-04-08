var mongoose = require('mongoose');

var connectionURI = 'mongodb://firethoughts:firethoughts123@127.0.0.1:27017/firethoughts_db';

mongoose.connect(connectionURI);

mongoose.connection.on('connected', function () {
    console.log('Mongoose connected to ' + connectionURI);
});

mongoose.connection.on('error', function (err) {
    console.log('Mongoose connection error: ' + err);
});

mongoose.connection.on('disconnected', function () {
    console.log('Mongoose disconnected');
});

process.on('SIGINT', function () {
    mongoose.connection.close(function () {
        console.log('Mongoose disconnected through app termination');
        process.exit(0);
    });
});
