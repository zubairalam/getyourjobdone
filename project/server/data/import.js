var fs = require('fs'),
    sys = require('sys'),
    spawn = require('child_process').spawn,
    db = 'firethoughts_db',
    jsonDirectory = './json';

console.log('--------------------------');
console.log('Loading JSON Fixtures from Directory %s', jsonDirectory);
var loadJson = function (dir, done) {
    fs.readdir(dir, function (error, list) {
        if (error) {
            return done(error);
        }
        var i = 0;
        (function next() {
            var file = list[i++];
            if (!file) {
                return done(null);
            }
            var fileName = file.replace('.json', '');
            file = dir + '/' + file;
            fs.stat(file, function (error, stat) {
                if (stat && stat.isDirectory()) {
                    walk(file, function (error) {
                        if (error) {
                            console.log(error);
                        }
                        next();
                    });
                } else {
                    // will probably need ordering soon.
                    console.log('Importing %s', file);
                    var loadFile = spawn('mongoimport', ['-d', db, '-c', fileName, '--file', file, '--jsonArray']);
                    loadFile.stdout.on('data', function (data) {
                        console.log(data.toString());
                    });
                    next();
                }
            });
        })();
    });
};
console.log('--------------------------');

loadJson(jsonDirectory, function (error) {
    if (error) {
        throw error;
    }
});