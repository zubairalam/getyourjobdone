var winston = require('winston'),
    path = require('path');

function Logger(){
    return winston.add(winston.transports.File, {
        filename: path.join(__dirname, 'errorLog.json'),
        maxsize: 1048576,
        maxFiles: 3,
        level: 'error'
    });
}
module.exports = new Logger();