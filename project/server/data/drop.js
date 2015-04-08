var fs = require('fs'),
    sys = require('sys'),
    spawn = require('child_process').spawn,
    db = 'firethoughts_db';

console.log('--------------------------');
console.log('Dropping Tables from database %s', db);
reset = spawn('mongo', [db, '--eval', 'db.dropDatabase();']);
reset.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
});
console.log('--------------------------');
