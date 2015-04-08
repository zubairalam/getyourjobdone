var fstream = require('fstream'),
    tar = require('tar'),
    zlib = require('zlib'),
    jsonDirectory = './json';

fstream.Reader({'path': jsonDirectory, 'type': 'Directory'})
    .pipe(tar.Pack())
    .pipe(zlib.Gzip())
    .pipe(fstream.Writer({'path': 'json.tar.gz'}));
