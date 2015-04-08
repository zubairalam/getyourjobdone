var fs = require('fs'),
    sys = require('sys'),
    spawn = require('child_process').spawn,
    db = 'firethoughts_db',
    jsonDirectory = 'json/';

console.log('--------------------------');
console.log('Tables from database %s', db);
var collections = spawn('mongo', [db, '--eval', 'db.getCollectionNames();']);
collections.stdout.on('data', function (data) {
    var raw_data = data.toString().replace('system.indexes', '');
    raw_data = raw_data.replace(/(connecting.*)/, '');
    raw_data = raw_data.replace(/(MongoDB.*)/, '');
    raw_data = raw_data.trim();
    collections = raw_data.split(",");
    for (var i = 0; i < collections.length; i++) {
        if(collections[i] !==''){
            console.log('Exporting: ' + collections[i]);
            var file = jsonDirectory + collections[i] + '.json';
            spawn('mongoexport', ['-d', db, '-c', collections[i], '-o', file]);
        }

    }
});
collections.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
});
